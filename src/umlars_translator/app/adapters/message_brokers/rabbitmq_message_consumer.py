from typing import Optional
import logging
import asyncio
import json
import uuid

from pydantic import ValidationError
import aio_pika
from kink import inject

from umlars_translator.core.deserialization.exceptions import UnsupportedSourceDataTypeError
from umlars_translator.app.exceptions import QueueUnavailableError, NotYetAvailableError, InputDataError
from umlars_translator.app.adapters.message_brokers.message_consumer import MessageConsumer
from umlars_translator.app.adapters.message_brokers import config as messaging_config
from umlars_translator.app.dtos.messages import ModelToTranslateMessage
from umlars_translator.app.dtos.input import UmlModelDTO
from umlars_translator.app import config as app_config
from umlars_translator.app.adapters.apis.rest_api_connector import RestApiConnector
from umlars_translator.app.utils.functions import retry_async
from umlars_translator.app.adapters.repositories.uml_model_repository import UmlModelRepository
from umlars_translator.app.adapters.message_brokers.rabbitmq_message_producer import RabbitMQProducer, create_failed_translation_message, create_successfull_translation_message, create_running_translation_message, send_translated_models_messages, send_translated_model_message
from umlars_translator.core.translator import ModelTranslator
from umlars_translator.core.deserialization.deserializer import ModelDeserializer


@inject
class RabbitMQConsumer(MessageConsumer):
    def __init__(self, queue_name: str, rabbitmq_host: str, repository_api_connector: RestApiConnector, uml_model_repository: UmlModelRepository, messaging_logger: Optional[logging.Logger] = None, model_translator: Optional[ModelTranslator] = None, message_producer: Optional[RabbitMQProducer] = None) -> None:
        self._logger = messaging_logger.getChild(self.__class__.__name__)
        self._logger.info(f"Initializing RabbitMQConsumer with queue '{queue_name}' and host '{rabbitmq_host}'")
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
        self._logger.info(f"Attempting to connect to RabbitMQ at host '{rabbitmq_host or self._rabbitmq_host}' and queue '{queue_name or self._queue_name}'")
        try:
            if self._connection and not self._connection.is_closed:
                self._logger.info("Closing existing RabbitMQ connection")
                await self._connection.close()

            rabbitmq_host = rabbitmq_host or self._rabbitmq_host
            queue_name = queue_name or self._queue_name

            self._connection = await aio_pika.connect_robust(
                host=rabbitmq_host,
                port=messaging_config.MESSAGE_BROKER_PORT,
                login=messaging_config.MESSAGE_BROKER_USER,
                password=messaging_config.MESSAGE_BROKER_PASSWORD
            )
            self._logger.info("Connected to RabbitMQ")

            self._channel = await self._connection.channel()
            self._logger.info("Channel opened")

            await self._channel.set_qos(prefetch_count=messaging_config.MESSAGE_BROKER_PREFETCH_COUNT)
            self._queue = await self._channel.declare_queue(queue_name, durable=is_queue_durable)
            self._logger.info(f"Declared queue '{queue_name}' with durability set to '{is_queue_durable}'")
        except aio_pika.exceptions.AMQPConnectionError as ex:
            error_message = f"Failed to connect to the RabbitMQ channel: {ex}"
            self._logger.error(error_message)
            raise NotYetAvailableError(error_message) from ex
        except asyncio.CancelledError as ex:
            error_message = f"Connecting to the RabbitMQ channel was cancelled: {ex}"
            self._logger.error(error_message)
            raise QueueUnavailableError(error_message) from ex
        except Exception as ex:
            self._logger.error(f"Unexpected error while connecting to RabbitMQ: {ex}")
            raise QueueUnavailableError("Unexpected error while connecting to RabbitMQ") from ex

    async def _callback(self, message: aio_pika.IncomingMessage) -> None:
        process_id = str(uuid.uuid4())
        self._logger.info("Callback execution started for message delivery tag %s. Process_id: %s", message.delivery_tag, process_id)

        async with message.process(ignore_processed=True):
            try:
                model_to_translate_message = self._deserialize_message(message)
                self._logger.debug(f"Deserialized message to {model_to_translate_message}")
                files_ids = model_to_translate_message.ids_of_source_files
                self._logger.info(f"Message contains {len(files_ids)} source file IDs")
            except Exception as ex:
                self._logger.error(f"Failed to deserialize message: {ex}")
                await message.reject(requeue=False)
                return

            running_translation_messages = map(lambda file_id: create_running_translation_message(file_id=file_id, process_id=process_id), files_ids)
            send_running_messages_coroutines = send_translated_models_messages(running_translation_messages)

            try:
                uml_model = await self.get_data_from_repository(model_to_translate_message.id)
                await send_running_messages_coroutines
                await self.process_message(uml_model, process_id=process_id)
                await message.ack()
                self._logger.info("Message with delivery tag %s acknowledged", message.delivery_tag)
            except Exception as ex:
                self._logger.error(f"Failed to process message: {ex}")
                failed_translation_messages = map(lambda file_id: create_failed_translation_message(file_id=file_id, process_id=process_id, error_message=f"Failed to process model. Error: {ex}"), files_ids)
                await send_running_messages_coroutines
                await send_translated_models_messages(failed_translation_messages)
                await message.reject(requeue=False)

    def _deserialize_message(self, message: aio_pika.IncomingMessage) -> ModelToTranslateMessage:
        self._logger.debug(f"Deserializing message body: {message.body}")
        try:
            message_data = json.loads(message.body)
            model_to_translate_message = ModelToTranslateMessage(**message_data)
            self._logger.info(f"Successfully deserialized message with ID {model_to_translate_message.id}")
            return model_to_translate_message
        except json.JSONDecodeError as ex:
            self._logger.error(f"Failed to decode JSON message: {ex}")
            raise InputDataError(f"Failed to decode JSON message: {ex}") from ex
        except ValidationError as ex:
            self._logger.error(f"Validation error during message deserialization: {ex}")
            raise InputDataError(f"Validation error during message deserialization: {ex}") from ex

    async def get_data_from_repository(self, model_to_translate_id: ModelToTranslateMessage) -> UmlModelDTO:
        self._logger.info(f"Starting message processing for model ID {model_to_translate_id}")
        models_repository_api_url = f"{app_config.REPOSITORY_API_URL}/{app_config.REPOSITORY_SERVICE_MODELS_ENDPOINT}/{model_to_translate_id}"

        self._logger.debug(f"Fetching data from repository API at {models_repository_api_url}")
        response_body = await self._repository_api_connector.get_data(models_repository_api_url)
        self._logger.debug(f"Received response from repository API")
        try:
            uml_model = UmlModelDTO(**response_body)
            self._logger.info(f"Deserialized UML model with ID: {uml_model.id}")
        except ValidationError as ex:
            error_message = f"Failed to deserialize response from the repository service: {ex}. Invalid structure."
            self._logger.error(error_message)
            raise InputDataError(error_message) from ex
        
        return uml_model

    async def process_message(self, uml_model: UmlModelDTO, process_id: str) -> None:
        # To avoid data races, we need to create a new instance of ModelTranslator for each message
        model_translator = ModelTranslator(model_deseializer=ModelDeserializer())
        scheduled_sending_coroutines = []
        try:
            for uml_file in uml_model.source_files:
                self._logger.info(f"Processing file: {uml_file.filename}")
                try:
                    model_translator.deserialize(data_sources=[uml_file.to_data_source()], clear_builder_afterwards=False, model_id=uml_model.id)
                    sending_success_message_coroutine = send_translated_model_message(create_successfull_translation_message(file_id=uml_file.id, process_id=process_id))
                    scheduled_sending_coroutines.append(sending_success_message_coroutine)
                    self._logger.info(f"File {uml_file.filename} was successfully deserialized")
                except Exception as ex:
                    error_message = f"Failed to deserialize file {uml_file.filename}: {ex}"
                    self._logger.error(error_message)
                    sending_fail_message_coroutine = send_translated_model_message(create_failed_translation_message(file_id=uml_file.id, process_id=process_id, error_message=error_message))
                    scheduled_sending_coroutines.append(sending_fail_message_coroutine)

        except UnsupportedSourceDataTypeError as ex:
            error_message = f"Failed to deserialize model: {ex}"
            self._logger.error(error_message)
            await asyncio.gather(*scheduled_sending_coroutines)
            raise InputDataError(error_message) from ex
        except Exception as ex:
            error_message = f"Failed to translate model: {ex}"
            self._logger.error(error_message)
            await asyncio.gather(*scheduled_sending_coroutines)
            raise InputDataError(error_message) from ex

        self._logger.info("Serializing translated model")
        translated_model = model_translator.serialize(to_string=False)
        await self._uml_model_repository.save(translated_model)
        model_translator.clear()
        self._logger.info(f"Model {uml_model.id} saved and translator state cleared")
        await asyncio.gather(*scheduled_sending_coroutines)

        self._logger.info(f"Successfully translated model: {translated_model.id}")

    async def start_consuming(self) -> None:
        self._logger.info("Starting to consume messages")
        try:
            await self.connect_channel()
            self._logger.info("Connected to channel, starting to consume")
            await self._queue.consume(self._callback)
        except aio_pika.exceptions.ConnectionClosed as ex:
            self._logger.error(f"Connection closed: {ex}")
            raise QueueUnavailableError("Connection closed by broker") from ex
        except QueueUnavailableError as ex:
            self._logger.error(f"Queue unavailable: {ex}")
            raise QueueUnavailableError("Queue unavailable") from ex
        except Exception as ex:
            self._logger.error(f"Unexpected error during message consumption: {ex}")
            raise QueueUnavailableError("Unexpected error during message consumption") from ex
