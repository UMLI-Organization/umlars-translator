from abc import ABC, abstractmethod


class MessageConsumer(ABC):
    @abstractmethod
    def start_consuming(self):
        ...
