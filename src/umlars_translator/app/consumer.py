from typing import Callable
from logging import Logger

import pika
import pika.channel

from src.umlars_translator.app import config


class RabbitMQConsumer:
    def __init__(self, logger: Logger, queue_name: str, rabbitmq_host: str):
        self._logger = logger.getChild(self.__class__.__name__)
        self._queue_name = queue_name
        self.connect_channel(rabbitmq_host)

    def connect_channel(self, rabbitmq_host: str) -> None:
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue_name, durable=True)
        self._channel.basic_consume(queue=self._queue_name, on_message_callback=self.__class__._callback, auto_ack=True)

    def _callback(self, channel: pika.channel.Channel, method, properties: dict, body: dict) -> None:
        self._logger(f"Called callback")
        try:
            # TODO translate
            channel.basic_ack(delivery_tag=method.delivery_tag)
        # TODO: specify exception and method argument
        except Exception as ex:
            channel.basic_nack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self._channel.start_consuming()
