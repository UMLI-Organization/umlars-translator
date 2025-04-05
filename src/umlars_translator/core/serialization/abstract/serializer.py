from abc import abstractmethod

from umlars_translator.core.utils.visitor import IModelVisitor
from umlars_translator.core.model.abstract.uml_model import IUmlModel


class UmlSerializer(IModelVisitor):
    @abstractmethod
    def serialize(self, model: IUmlModel, to_string: bool) -> str:
        pass
