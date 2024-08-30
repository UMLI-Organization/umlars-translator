import json
from typing import Optional
import logging

from kink import inject
import aio_pika
from contextlib import asynccontextmanager

from src.umlars_translator.app.adapters.message_brokers.message_producer import MessageProducer
from src.umlars_translator.app.adapters.message_brokers import config
from src.umlars_translator.app.exceptions import QueueUnavailableError


@inject(alias=MessageProducer)
class RabbitMQProducer(MessageProducer):
    def __init__(self, queue_name: str = config.MESSAGE_BROKER_QUEUE_TRANSLATED_MODELS_NAME, rabbitmq_host: str = config.MESSAGE_BROKER_HOST, messaging_logger: Optional[logging.Logger] = None) -> None:
        self._logger = messaging_logger.getChild(self.__class__.__name__)
        self._queue_name = queue_name
        self._rabbitmq_host = rabbitmq_host
        self._connection = None
        self._channel = None
        self._queue = None

    @asynccontextmanager
    async def connect_channel(self, rabbitmq_host: Optional[str] = None, queue_name: Optional[str] = None, is_queue_durable: bool = True, reset_connection: bool = False) -> None:
        try:
            if not self._connection or reset_connection or self._connection.is_closed:
                rabbitmq_host = rabbitmq_host or self._rabbitmq_host
                queue_name = queue_name or self._queue_name

                self._connection = await aio_pika.connect_robust(
                    host=rabbitmq_host,
                    port=config.MESSAGE_BROKER_PORT,
                    login=config.MESSAGE_BROKER_USER,
                    password=config.MESSAGE_BROKER_PASSWORD,
                )
            self._channel = await self._connection.channel()
            self._queue = await self._channel.declare_queue(queue_name, durable=is_queue_durable)
            self._logger.info("Connected to RabbitMQ channel and queue")
            yield self._channel
        except aio_pika.exceptions.AMQPConnectionError as ex:
            self._logger.error(f"Failed to connect to the channel: {ex}")
            raise QueueUnavailableError("Failed to connect to the channel") from ex
        except Exception as ex:
            self._logger.error(f"Unexpected error: {ex}")
            raise QueueUnavailableError("Unexpected error while connecting to the channel") from ex
        finally:
            if self._connection and not self._connection.is_closed:
                await self._connection.close()

    async def send_message(self, message_data: dict) -> None:
        async with self.connect_channel() as channel:
            try:
                message_body = json.dumps(message_data).encode()
                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body=message_body,
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    ),
                    routing_key=self._queue_name,
                )
                self._logger.info("Message sent")
            except Exception as ex:
                self._logger.error(f"Error while sending message: {ex}")
                raise ValueError(f"Error while sending message: {ex}") from ex


async def send_translated_model_message(message_data: dict, producer: Optional[MessageProducer] = None, queue_name: str = config.MESSAGE_BROKER_QUEUE_TRANSLATED_MODELS_NAME) -> None:
    try:
        if producer is None:
            producer = RabbitMQProducer(queue_name=queue_name, rabbitmq_host=config.MESSAGE_BROKER_HOST)
        await producer.send_message(message_data)
    except Exception as ex:
        raise ValueError(f"Error while sending message: {ex}") from ex


def create_successfull_translation_message(uml_model_id: str) -> dict:
    return {
        "model_id": uml_model_id,
        "status": config.TranslationStatusEnum.FINISHED,
        "message": "Model was successfully translated"
    }


def create_failed_translation_message(uml_model_id: str, error_message: str) -> dict:
    return {
        "model_id": uml_model_id,
        "status": config.TranslationStatusEnum.FAILED,
        "message": error_message
    }


def create_partial_success_translation_message(uml_model_id: str, error_message: str) -> dict:
    return {
        "model_id": uml_model_id,
        "status": config.TranslationStatusEnum.PARTIAL_SUCCESS,
        "message": error_message
    }


def create_running_translation_message(uml_model_id: str) -> dict:
    return {
        "model_id": uml_model_id,
        "status": config.TranslationStatusEnum.RUNNING,
        "message": "Model translation is in progress"
    }
