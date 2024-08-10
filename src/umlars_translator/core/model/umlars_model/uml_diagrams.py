from typing import TYPE_CHECKING
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from dataclass_wizard import property_wizard

from src.umlars_translator.core.model.umlars_model.uml_element import UmlElement, UmlNamedElement
from src.umlars_translator.core.model.umlars_model.uml_elements import UmlClass, UmlLifeline, UmlAssociationEnd, UmlAssociationBase, UmlInterface, UmlPackage, UmlPrimitiveType, UmlAttribute, UmlOperation, UmlLifeline, UmlAssociationEnd, UmlAssociationBase, UmlAssociationBase




@dataclass
#TODO: inheirit from JSONSerializable / JSONWIzard from property_wizard ?
class UmlDiagram(UmlNamedElement, metaclass=property_wizard):
    @abstractmethod
    def add_element(self, element: UmlElement) -> None:
        ...


@dataclass
class UmlClassDiagram(UmlDiagram):
    classes: list[UmlClass] = field(default_factory=list)
    associations: list[UmlAssociationBase] = field(default_factory=list)
    generalizations: list[UmlAssociationBase] = field(default_factory=list)
    dependencies: list[UmlAssociationBase] = field(default_factory=list)
    interfaces: list[UmlInterface] = field(default_factory=list)
    packages: list[UmlPackage] = field(default_factory=list)
    primitive_types: list[UmlPrimitiveType] = field(default_factory=list)
    attributes: list[UmlAttribute] = field(default_factory=list)
    operations: list[UmlOperation] = field(default_factory=list)

    def add_element(self, element: UmlElement) -> None:
        if isinstance(element, UmlClass):
            self.classes.append(element)
        elif isinstance(element, UmlAssociationBase):
            self.associations.append(element)
        elif isinstance(element, UmlInterface):
            self.interfaces.append(element)
        elif isinstance(element, UmlPackage):
            self.packages.append(element)
        elif isinstance(element, UmlPrimitiveType):
            self.primitive_types.append(element)
        elif isinstance(element, UmlAttribute):
            self.attributes.append(element)
        elif isinstance(element, UmlOperation):
            self.operations.append(element)
        else:
            raise NotImplementedError(f"Element {element} is not supported in UmlClassDiagram.")



@dataclass
class UmlSequenceDiagram(UmlDiagram):
    lifelines: list[UmlLifeline] = field(default_factory=list)
    messages: list[UmlAssociationEnd] = field(default_factory=list)
    fragments: list[UmlAssociationBase] = field(default_factory=list)
    combined_fragments: list[UmlAssociationBase] = field(default_factory=list)
    interaction_operands: list[UmlAssociationBase] = field(default_factory=list)

    def add_element(self, element: UmlElement) -> None:
        if isinstance(element, UmlLifeline):
            self.lifelines.append(element)
        elif isinstance(element, UmlAssociationEnd):
            self.messages.append(element)
        elif isinstance(element, UmlAssociationBase):
            self.fragments.append(element)
        elif isinstance(element, UmlAssociationBase):
            self.combined_fragments.append(element)
        elif isinstance(element, UmlAssociationBase):
            self.interaction_operands.append(element)
        else:
            raise NotImplementedError(f"Element {element} is not supported in UmlSequenceDiagram.")
