from abc import ABC, abstractmethod
from typing import List, Union, TYPE_CHECKING

from src.umlars_translator.core.utils.visitor import IVisitable, IVisitor
from src.umlars_translator.core.model.abstract.uml_elements import IUmlModelElements
from src.umlars_translator.core.model.abstract.uml_diagrams import IUmlDiagrams


class IUmlModel(IVisitable, ABC):
    def accept(self, visitor: IVisitor):
        return visitor.visit_uml_model(self)

    @property
    @abstractmethod
    def elements(self) -> IUmlModelElements:
        ...

    @property
    @abstractmethod
    def diagrams(self) -> IUmlDiagrams:
        ...
