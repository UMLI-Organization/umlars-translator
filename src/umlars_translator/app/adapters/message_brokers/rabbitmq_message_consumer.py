from typing import Optional
import logging
import asyncio
import aiohttp
import json

import aio_pika
from kink import inject
from src.umlars_translator.app.exceptions import QueueUnavailableError
from src.umlars_translator.app.adapters.message_brokers.message_consumer import MessageConsumer
from src.umlars_translator.app.adapters.message_brokers import config as messaging_config
from src.umlars_translator.app.dtos.messages import ModelToTranslateMessage
from src.umlars_translator.app.dtos.input import UmlModel
from src.umlars_translator.app import config as app_config


@inject
class RabbitMQConsumer(MessageConsumer):
    def __init__(self, queue_name: str, rabbitmq_host: str, messaging_logger: Optional[logging.Logger] = None) -> None:
        self._logger = messaging_logger.getChild(self.__class__.__name__)
        self._queue_name = queue_name
        self._rabbitmq_host = rabbitmq_host
        self._connection = None
        self._channel = None
        self._queue = None

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
        except (aio_pika.exceptions.AMQPConnectionError, asyncio.CancelledError) as ex:
            self._logger.error(f"Failed to connect to the channel: {ex}")
            raise QueueUnavailableError("Failed to connect to the channel") from ex
        except Exception as ex:
            self._logger.error(f"Unexpected error: {ex}")
            raise QueueUnavailableError("Unexpected error while connecting to the channel") from ex

    async def _callback(self, message: aio_pika.IncomingMessage) -> None:
        async with message.process(ignore_processed=True):
            self._logger.info("Called callback from logger")
            try:
                # Replace with actual processing logic
                await self.process_message(message)
                await message.ack()
                self._logger.info("Message acknowledged")
            except Exception as ex:
                self._logger.error(f"Failed to process message: {ex}")
                await message.reject(requeue=False)

    async def process_message(self, message: aio_pika.IncomingMessage) -> None:
        message_data = json.loads(message.body)
        model_to_translate_message = ModelToTranslateMessage(**message_data)
        aiohttp_client = aiohttp.ClientSession()
        async with aiohttp_client:
            models_repository_api_url = f"{app_config.REPOSITORY_API_URL}/{app_config.REPOSITORY_SERVICE_MODELS_ENDPOINT}/{model_to_translate_message.id}"

            async with aiohttp_client.get(models_repository_api_url) as response:
                response_body = await response.text()
                self._logger.info(f"Response from translation service: {response_body}")
                uml_model = UmlModel(**json.loads(response_body))
                self._logger.info(f"Response from translation service: {uml_model}")

        # TODO: Add translation logic or other processing logic here
        self._logger.info(f"Processed message: {message.body}")

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
