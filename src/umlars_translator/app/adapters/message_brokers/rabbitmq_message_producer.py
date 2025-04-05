import json
from typing import Optional, Iterable, Coroutine, List
import logging
import asyncio

from kink import inject
import aio_pika
from contextlib import asynccontextmanager

from umlars_translator.app.adapters.message_brokers.message_producer import MessageProducer
from umlars_translator.app.adapters.message_brokers import config
from umlars_translator.app.exceptions import QueueUnavailableError
from umlars_translator.app.dtos.messages import ProcessStatusEnum, TranslatedFileMessage


@inject(alias=MessageProducer)
class RabbitMQProducer(MessageProducer):
    def __init__(self, queue_name: str = config.MESSAGE_BROKER_QUEUE_TRANSLATED_MODELS_NAME, rabbitmq_host: str = config.MESSAGE_BROKER_HOST, messaging_logger: Optional[logging.Logger] = None) -> None:
        self._logger = messaging_logger.getChild(self.__class__.__name__)
        self._queue_name = queue_name
        self._rabbitmq_host = rabbitmq_host
        self._connection = None
        self._channel = None
        self._queue = None
        self._logger.info(f"RabbitMQProducer initialized with queue '{queue_name}' and host '{rabbitmq_host}'")

    @asynccontextmanager
    async def connect_channel(self, rabbitmq_host: Optional[str] = None, queue_name: Optional[str] = None, is_queue_durable: bool = True, reset_connection: bool = False) -> None:
        try:
            if not self._connection or reset_connection or self._connection.is_closed:
                rabbitmq_host = rabbitmq_host or self._rabbitmq_host
                queue_name = queue_name or self._queue_name
                self._logger.info(f"Connecting to RabbitMQ at host '{rabbitmq_host}' with queue '{queue_name}'")

                self._connection = await aio_pika.connect_robust(
                    host=rabbitmq_host,
                    port=config.MESSAGE_BROKER_PORT,
                    login=config.MESSAGE_BROKER_USER,
                    password=config.MESSAGE_BROKER_PASSWORD,
                )
                self._logger.info("RabbitMQ connection established")
            else:
                self._logger.info("Using existing RabbitMQ connection")

            self._channel = await self._connection.channel()
            self._queue = await self._channel.declare_queue(queue_name, durable=is_queue_durable)
            self._logger.info(f"Connected to RabbitMQ channel and declared queue '{queue_name}' with durability '{is_queue_durable}'")
            yield self._channel
        except aio_pika.exceptions.AMQPConnectionError as ex:
            self._logger.error(f"Failed to connect to the RabbitMQ channel: {ex}")
            raise QueueUnavailableError("Failed to connect to the RabbitMQ channel") from ex
        except Exception as ex:
            self._logger.error(f"Unexpected error while connecting to RabbitMQ: {ex}")
            raise QueueUnavailableError("Unexpected error while connecting to RabbitMQ") from ex
        finally:
            if self._connection and not self._connection.is_closed:
                self._logger.info("Closing RabbitMQ connection")
                await self._connection.close()
                self._logger.info("RabbitMQ connection closed")

    async def send_message(self, message_data: dict) -> None:
        self._logger.info(f"Preparing to send message: {message_data}")
        async with self.connect_channel() as channel:
            try:
                message_body = json.dumps(message_data).encode()
                self._logger.debug(f"Encoded message body: {message_body}")

                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body=message_body,
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    ),
                    routing_key=self._queue_name,
                )
                self._logger.info(f"Message sent to queue '{self._queue_name}'")
            except Exception as ex:
                self._logger.error(f"Error while sending message to RabbitMQ: {ex}")
                raise ValueError(f"Error while sending message to RabbitMQ: {ex}") from ex


async def send_translated_model_message(message_data: dict, producer: Optional[MessageProducer] = None, queue_name: str = config.MESSAGE_BROKER_QUEUE_TRANSLATED_MODELS_NAME) -> Coroutine:
    try:
        if producer is None:
            producer = RabbitMQProducer(queue_name=queue_name, rabbitmq_host=config.MESSAGE_BROKER_HOST)
        return await producer.send_message(message_data)
    except Exception as ex:
        logging.error(f"Failed to send translated model message: {ex}")
        raise ValueError(f"Error while sending message: {ex}") from ex


async def send_translated_models_messages(messages_data: Iterable[dict], producer: Optional[MessageProducer] = None, queue_name: str = config.MESSAGE_BROKER_QUEUE_TRANSLATED_MODELS_NAME) -> Coroutine:
    logging.info(f"Sending translated model messages to queue '{queue_name}'")
    return asyncio.gather(*[send_translated_model_message(message_data, producer, queue_name) for message_data in messages_data])


def create_successfull_translation_message(file_id: str, process_id: str) -> dict:
    logging.debug(f"Creating successful translation message for file ID: {file_id}")
    return TranslatedFileMessage(
        id=file_id,
        process_id=process_id,
        state=ProcessStatusEnum.FINISHED,
        message="Model was successfully translated"
    ).model_dump()


def create_failed_translation_message(file_id: str, process_id: str, error_message: Optional[str] = None) -> dict:
    logging.debug(f"Creating failed translation message for file ID: {file_id} with error: {error_message}")
    return TranslatedFileMessage(
        id=file_id,
        process_id=process_id,
        state=ProcessStatusEnum.FAILED,
        message=error_message
    ).model_dump()


def create_partial_success_translation_message(file_id: str, process_id: str, error_message: Optional[str] = None) -> dict:
    logging.debug(f"Creating partial success translation message for file ID: {file_id} with error: {error_message}")
    return TranslatedFileMessage(
        id=file_id,
        process_id=process_id,
        state=ProcessStatusEnum.PARTIAL_SUCCESS,
        message=error_message
    ).model_dump()


def create_running_translation_message(file_id: str, process_id: str) -> dict:
    logging.debug(f"Creating running translation message for file ID: {file_id}")
    return TranslatedFileMessage(
        id=file_id,
        process_id=process_id,
        state=ProcessStatusEnum.RUNNING,
        message="Model translation is in progress"
    ).model_dump()
