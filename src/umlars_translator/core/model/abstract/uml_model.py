from abc import ABC, abstractmethod
from typing import List, Union, TYPE_CHECKING

from src.umlars_translator.core.utils.visitor import IVisitable, IVisitor
if TYPE_CHECKING:
    from src.umlars_translator.core.model.abstract.uml_diagrams import IUmlClassDiagram, IUmlSequenceDiagram
    from src.umlars_translator.core.model.abstract.uml_elements import IUmlModelElements


class IUmlDiagrams(IVisitable, ABC):
    def accept(self, visitor: IVisitor):
        return visitor.visit_uml_diagrams(self)

    @property
    @abstractmethod
    def class_diagrams(self) -> List["IUmlClassDiagram"]:
        ...

    @property
    @abstractmethod
    def sequence_diagrams(self) -> List["IUmlSequenceDiagram"]:
        ...


class IUmlModel(IVisitable, ABC):
    def accept(self, visitor: IVisitor):
        return visitor.visit_uml_model(self)

    @property
    @abstractmethod
    def elements(self) -> IUmlModelElements:
        ...
