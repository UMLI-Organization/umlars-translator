from abc import ABC, abstractmethod


class IVisitor(ABC):
    ...


class IVisitable(ABC):
    @abstractmethod
    def accept(self, visitor: IVisitor):
        pass
