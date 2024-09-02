from abc import ABC, abstractmethod


class MessageProducer(ABC):
    @abstractmethod
    def send_message(self):
        ...

    @abstractmethod
    def connect_channel(self):
        ...
