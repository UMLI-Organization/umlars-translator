from typing import Optional
import logging
import socket
# TODO: remove after successfull async implementation
import time

import pika
from kink import inject

from src.umlars_translator.app.exceptions import QueueUnavailableError
from src.umlars_translator.app.adapters.message_brokers.message_consumer import MessageConsumer


@inject
class RabbitMQConsumer(MessageConsumer):
    def __init__(self, queue_name: str, rabbitmq_host: str, messaging_logger: Optional[logging.Logger] = None) -> None:
        self._logger = messaging_logger.getChild(self.__class__.__name__)
        self._queue_name = queue_name
        self.connect_channel(rabbitmq_host)

    def connect_channel(self, rabbitmq_host: str) -> None:
        try:
            self._connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
            self._channel = self._connection.channel()
            self._queue = self._channel.queue_declare(queue=self._queue_name, durable=True)
            rv = self._channel.basic_consume(queue=self._queue_name, on_message_callback=self._callback)
            self._logger.info(f"Connected channgel -rv: {rv}")
            # print(f"Connected channgel -rv: {rv}")
        except socket.gaierror as ex:
            self._logger.error(f"Failed to connect to the channel: {ex}")
            # print(f"Failed to connect to the channel: {ex}")
            raise QueueUnavailableError("Failed to connect to the channel") from ex

    def _callback(self, channel: pika.channel.Channel, method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes) -> None:
        self._logger.error(f"Called callback from logger")
        # TODO: remove after successfull async implementation
        time.sleep(10)

        self._logger.error(f"Called callback - after sleep")
        try:
            # TODO translate
            channel.basic_ack(delivery_tag=method.delivery_tag)
        # TODO: specify exception and method argument
        except Exception as ex:
            channel.basic_nack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        try:
            self._channel.start_consuming()
        except pika.exceptions.ConnectionClosedByBroker as ex:
            self._logger.error(f"Connection closed by broker: {ex}")
            raise QueueUnavailableError("Connection closed by broker") from ex
