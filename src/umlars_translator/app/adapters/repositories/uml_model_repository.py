from abc import ABC, abstractmethod

from umlars_translator.app.dtos.uml_model import UmlModel


class UmlModelRepository(ABC):
    @abstractmethod
    def get(self, model_id: str) -> UmlModel:
        ...

    @abstractmethod
    def save(self, uml_model: UmlModel) -> UmlModel:
        ...
