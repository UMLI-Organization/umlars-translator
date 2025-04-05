from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from umlars_translator.core.model.abstract.uml_model import IUmlModel
from umlars_translator.core.model.umlars_model.uml_elements import UmlClass, UmlModelElements, UmlAssociationBase, UmlVisibilityEnum, UmlPackage, UmlInterface, UmlInteraction, UmlLifeline, UmlNamedElement
from umlars_translator.core.model.umlars_model.mixins import RegisteredInBuilderMixin
from umlars_translator.core.model.umlars_model.uml_diagrams import UmlDiagrams


class UmlModel(UmlNamedElement, IUmlModel):
    def __init__(self, builder: Optional['UmlModelBuilder'] = None, name: Optional[str] = None,  visibility: Optional[UmlVisibilityEnum] = None, elements: Optional[UmlModelElements] = None, diagrams: Optional[UmlDiagrams] = None, metadata: Optional[dict] = None, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, builder=builder, name=name, visibility=visibility, **kwargs)
        self.metadata = metadata or {}
        self.elements = elements or UmlModelElements()
        self.diagrams = diagrams or UmlDiagrams()

    @property
    def metadata(self) -> dict:
        return self._metadata

    @metadata.setter
    def metadata(self, new_metadata: dict):
        self._metadata = new_metadata

    @property
    def elements(self) -> UmlModelElements:
        return self._elements
    
    @elements.setter
    def elements(self, new_elements: UmlModelElements):
        self._elements = new_elements
        if self._elements and self.builder:
            for class_element in self._elements.classes:
                self.builder.add_class(class_element)
            for association in self._elements.associations:
                self.builder.add_association(association)
            for interface in self._elements.interfaces:
                self.builder.add_class(interface)
            for package in self._elements.packages:
                self.builder.add_class(package)
            for interaction in self._elements.interactions:
                self.builder.add_class(interaction)

    @property
    def diagrams(self) -> UmlDiagrams:
        return self._diagrams
    
    @diagrams.setter
    def diagrams(self, new_diagrams: UmlDiagrams):
        self._diagrams = new_diagrams
        if self._diagrams and self.builder:
            for diagram in self._diagrams.class_diagrams:
                self.builder.add_diagram(diagram)
            for diagram in self._diagrams.sequence_diagrams:
                self.builder.add_diagram(diagram)

    def add_class(self, uml_class: UmlClass):
        uml_class.builder = self.builder
        self.builder.add_class(uml_class)

    def add_lifeline(self, lifeline: UmlLifeline):
        lifeline.builder = self.builder
        self.builder.add_lifeline(lifeline)

    def add_association(self, association: UmlAssociationBase):
        association.builder = self.builder
        self.builder.add_association(association)

    # TODO: Add other proxy methods as needed or maybe move to the IUmlModel interface
