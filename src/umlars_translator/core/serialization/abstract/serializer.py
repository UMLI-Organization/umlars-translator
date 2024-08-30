from abc import abstractmethod

from src.umlars_translator.core.utils.visitor import IModelVisitor
from src.umlars_translator.core.model.abstract.uml_model import IUmlModel


class UmlSerializer(IModelVisitor):
    @abstractmethod
    def serialize(self, model: IUmlModel) -> str:
        pass
