from abc import ABC, abstractmethod

from umlars_translator.app.dtos.uml_model import UmlModel


class UmlModelRepository(ABC):
    @abstractmethod
    async def get(self, model_id: str) -> UmlModel:
        ...

    @abstractmethod
    async def save(self, uml_model: UmlModel) -> UmlModel:
        ...
