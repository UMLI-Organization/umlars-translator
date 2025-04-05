from abc import ABC, abstractmethod
from typing import List, Union, TYPE_CHECKING

from umlars_translator.core.utils.visitor import IVisitable, IVisitor

from umlars_translator.core.model.abstract.uml_elements import IUmlElement, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration, IUmlPrimitiveType, IUmlAssociation, IUmlDirectedAssociation, IUmlGeneralization, IUmlDependency, IUmlRealization, IUmlInteraction


class IUmlDiagram(IVisitable, ABC):
    @abstractmethod
    def add_element(self, element: IUmlElement) -> None:
        ...


class IUmlClassDiagramElements(IVisitable, ABC):
    def accept(self, visitor: IVisitor):
        return visitor.visit_uml_class_diagram_elements(self)

    @property
    @abstractmethod
    def classes() -> List[IUmlClass]:
        ...

    @property
    @abstractmethod
    def interfaces() -> List[IUmlInterface]:
        ...

    @property
    @abstractmethod
    def data_types() -> List[IUmlDataType]:
        ...

    @property
    @abstractmethod
    def enumerations() -> List[IUmlEnumeration]:
        ...

    @property
    @abstractmethod
    def primitive_types() -> List[IUmlPrimitiveType]:
        ...

    @property
    @abstractmethod
    def associations() -> List[Union["IUmlAssociation", "IUmlDirectedAssociation"]]:
        ...

    @property
    @abstractmethod
    def generalizations() -> List[IUmlGeneralization]:
        ...

    @property
    @abstractmethod
    def dependencies() -> List[IUmlDependency]:
        ...

    @property
    @abstractmethod
    def realizations() -> List[IUmlRealization]:
        ...


class IUmlSequenceDiagramElements(IVisitable, ABC):
    def accept(self, visitor: IVisitor):
        return visitor.visit_uml_sequence_diagram_elements(self)

    @property
    @abstractmethod
    def interactions() -> List[IUmlInteraction]:
        ...


class IUmlClassDiagram(IUmlDiagram):
    def accept(self, visitor: IVisitor):
        return visitor.visit_uml_class_diagram(self)

    @property
    @abstractmethod
    def elements(self) -> IUmlClassDiagramElements:
        ...


class IUmlSequenceDiagram(IUmlDiagram):
    def accept(self, visitor: IVisitor):
        return visitor.visit_uml_sequence_diagram(self)

    @property
    @abstractmethod
    def elements(self) -> IUmlSequenceDiagramElements:
        ...


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
