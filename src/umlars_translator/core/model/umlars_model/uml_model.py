from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass, field

from dataclass_wizard import property_wizard, JSONWizard

from src.umlars_translator.core.model.abstract.uml_model import IUmlModel
from src.umlars_translator.core.model.umlars_model.uml_elements import UmlClass, UmlLifeline, UmlAssociationBase, UmlVisibilityEnum, UmlPackage, UmlInterface, UmlInteraction
from src.umlars_translator.core.model.umlars_model.mixins import RegisteredInBuilderMixin
from src.umlars_translator.core.model.umlars_model.uml_diagrams import UmlDiagram


@dataclass
class UmlModel(RegisteredInBuilderMixin, IUmlModel, metaclass=property_wizard):
    metadata: dict = field(default_factory=dict)
    name: Optional[str] = None
    visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC

    packages: list[UmlPackage] = field(default_factory=list)
    classes: list[UmlClass] = field(default_factory=list)
    interfaces: list[UmlInterface] = field(default_factory=list)
    associations: list[UmlAssociationBase] = field(default_factory=list)
    interactions: list[UmlInteraction] = field(default_factory=list)


    diagrams: list[UmlDiagram] = field(default_factory=list)
        
 

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



