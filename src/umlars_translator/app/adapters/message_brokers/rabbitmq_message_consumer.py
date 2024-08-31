from typing import Optional
import logging
import asyncio
import json

from pydantic import ValidationError
import aio_pika
from kink import inject

from src.umlars_translator.core.deserialization.exceptions import UnsupportedSourceDataTypeError
from src.umlars_translator.app.exceptions import QueueUnavailableError, NotYetAvailableError, InputDataError
from src.umlars_translator.app.adapters.message_brokers.message_consumer import MessageConsumer
from src.umlars_translator.app.adapters.message_brokers import config as messaging_config
from src.umlars_translator.app.dtos.messages import ModelToTranslateMessage
from src.umlars_translator.app.dtos.input import UmlModelDTO
from src.umlars_translator.app import config as app_config
from src.umlars_translator.app.adapters.apis.rest_api_connector import RestApiConnector
from src.umlars_translator.app.utils.functions import retry_async
from src.umlars_translator.app.adapters.repositories.uml_model_repository import UmlModelRepository
from src.umlars_translator.app.adapters.message_brokers.rabbitmq_message_producer import RabbitMQProducer, create_failed_translation_message, create_successfull_translation_message, create_running_translation_message, send_translated_models_messages, send_translated_model_message
from src.umlars_translator.core.translator import ModelTranslator


@inject
class RabbitMQConsumer(MessageConsumer):
    def __init__(self, queue_name: str, rabbitmq_host: str, repository_api_connector: RestApiConnector, uml_model_repository: UmlModelRepository, messaging_logger: Optional[logging.Logger] = None, model_translator: Optional[ModelTranslator] = None, message_producer: Optional[RabbitMQProducer] = None) -> None:
        self._logger = messaging_logger.getChild(self.__class__.__name__)
        self._repository_api_connector = repository_api_connector
        self._model_translator = model_translator or ModelTranslator()
        self._uml_model_repository = uml_model_repository
        self._message_producer = message_producer or RabbitMQProducer(queue_name=messaging_config.MESSAGE_BROKER_TRANSLATED_MODELS_QUEUE_NAME, rabbitmq_host=messaging_config.MESSAGE_BROKER_HOST)
        self._queue_name = queue_name
        self._rabbitmq_host = rabbitmq_host
        self._connection = None
        self._channel = None
        self._queue = None

    @retry_async(exception_class_raised_when_all_attempts_failed=QueueUnavailableError)
    async def connect_channel(self, rabbitmq_host: Optional[str] = None, queue_name: Optional[str] = None, is_queue_durable: bool = True) -> None:
        try:
            if self._connection and not self._connection.is_closed:
                await self._connection.close()

            rabbitmq_host = rabbitmq_host or self._rabbitmq_host
            queue_name = queue_name or self._queue_name

            # TODO: add here event loop as argument to connect_robust
            self._connection = await aio_pika.connect_robust(host=rabbitmq_host, port=messaging_config.MESSAGE_BROKER_PORT, login=messaging_config.MESSAGE_BROKER_USER, password=messaging_config.MESSAGE_BROKER_PASSWORD)
            self._channel = await self._connection.channel()
            await self._channel.set_qos(prefetch_count=messaging_config.MESSAGE_BROKER_PREFETCH_COUNT)
            self._queue = await self._channel.declare_queue(queue_name, durable=is_queue_durable)
            self._logger.info("Connected to RabbitMQ channel and queue")
        except aio_pika.exceptions.AMQPConnectionError as ex:
            error_message = f"Failed to connect to the channel: {ex}"
            self._logger.error(error_message)
            raise NotYetAvailableError(error_message) from ex
        except asyncio.CancelledError as ex:
            error_message = f"Connecting to the channel was cancelled: {ex}"
            self._logger.error(error_message)
            raise QueueUnavailableError(error_message) from ex
        except Exception as ex:
            self._logger.error(f"Unexpected error: {ex}")
            raise QueueUnavailableError("Unexpected error while connecting to the channel") from ex

    async def _callback(self, message: aio_pika.IncomingMessage) -> None:
        self._logger.info("Callback execution started")

        async with message.process(ignore_processed=True):
            try:
                model_to_translate_message = self._deserialize_message(message)
                files_ids = model_to_translate_message.ids_of_source_files
            except Exception as ex:
                self._logger.error(f"Failed to deserialize message: {ex}")
                await message.reject(requeue=False)
                return

            running_translation_messages = map(lambda file_id: create_running_translation_message(file_id=file_id), files_ids)
            send_running_messages_coroutines = asyncio.gather(*send_translated_models_messages(running_translation_messages, self._message_producer))

            try:
                await self.process_message(model_to_translate_message)
                await message.ack()
                await send_running_messages_coroutines
                self._logger.info("Message acknowledged")
            except Exception as ex:
                self._logger.error(f"Failed to process message: {ex}")
                failed_translation_messages = map(lambda file_id: create_failed_translation_message(file_id=file_id, error_message=f"Failed to process model. Error: {ex}"), files_ids)
                await send_running_messages_coroutines
                await send_translated_models_messages(failed_translation_messages, self._message_producer)
                await message.reject(requeue=False)

    def _deserialize_message(self, message: aio_pika.IncomingMessage) -> ModelToTranslateMessage:
        message_data = json.loads(message.body)
        model_to_translate_message = ModelToTranslateMessage(**message_data)
        self._logger.info(f"Processing message: {model_to_translate_message}")
        return model_to_translate_message

    async def process_message(self, model_to_translate_message: ModelToTranslateMessage) -> None:
        # TODO: add filter - only changed or added files
        models_repository_api_url = f"{app_config.REPOSITORY_API_URL}/{app_config.REPOSITORY_SERVICE_MODELS_ENDPOINT}/{model_to_translate_message.id}"

        response_body = await self._repository_api_connector.get_data(models_repository_api_url)
        self._logger.debug(f"Response from repo service: {response_body}")
        try:
            uml_model = UmlModelDTO(**response_body)
            self._logger.info(f"Deserialized model with id: {uml_model.id}")
        except ValidationError as ex:
            error_message = f"Failed to deserialize response from the repository service: {ex}. Invalid structure."
            self._logger.error(error_message)
            raise InputDataError(error_message) from ex

        scheduled_sending_coroutines = []
        try:
            for uml_file in uml_model.source_files:
                self._logger.info(f"Processing file: {uml_file.filename}")
                try:
                    self._model_translator.deserialize(data_sources=[uml_file.to_data_source()], clear_builder_afterwards=False)
                    sending_success_message_coroutine = send_translated_model_message(create_successfull_translation_message(file_id=uml_file.id), self._message_producer)
                    scheduled_sending_coroutines.append(sending_success_message_coroutine)
                    self._logger.info(f"File {uml_file.filename} was successfully deserialized")
                except Exception as ex:
                    error_message = f"Failed to deserialize file: {ex}"
                    self._logger.error(error_message)
                    sending_fail_message_coroutine = send_translated_model_message(create_failed_translation_message(file_id=uml_file.id, error_message=error_message), self._message_producer)
                    scheduled_sending_coroutines.append(sending_fail_message_coroutine)

            translated_model = self._model_translator.serialize()
            await self._uml_model_repository.save(translated_model)
            self._model_translator.clear()
            await asyncio.gather(*scheduled_sending_coroutines)

        except UnsupportedSourceDataTypeError as ex:
            error_message = f"Failed to deserialize model: {ex}"
            self._logger.error(error_message)
            raise InputDataError(error_message) from ex
        except Exception as ex:
            error_message = f"Failed to translate model: {ex}"
            self._logger.error(error_message)
            raise InputDataError(error_message) from ex

        self._logger.info(f"Translated model: {translated_model}")

    async def start_consuming(self) -> None:
        try:
            await self.connect_channel()
            await self._queue.consume(self._callback)
            self._logger.info("Starting to consume messages")
        except aio_pika.exceptions.ConnectionClosed as ex:
            self._logger.error(f"Connection closed: {ex}")
            raise QueueUnavailableError("Connection closed by broker") from ex
        except QueueUnavailableError as ex:
            self._logger.error(f"Queue unavailable: {ex}")
            raise QueueUnavailableError("Queue unavailable") from ex
        except Exception as ex:
            self._logger.error(f"Unexpected error during messages consumtion: {ex}")
            raise QueueUnavailableError("Unexpected error during messages consumption") from ex
