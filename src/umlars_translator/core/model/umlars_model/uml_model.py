from typing import Optional
from dataclasses import dataclass

from src.umlars_translator.core.model.abstract.uml_model import IUmlModel
from src.umlars_translator.core.model.umlars_model.uml_model_builder import UmlModelBuilder
from src.umlars_translator.core.model.umlars_model.uml_elements import UmlClass, UmlLifeline, UmlAssociationBase


@dataclass
class UmlModel(IUmlModel):
    def __init__(self, builder: Optional[UmlModelBuilder] = None) -> None:
        self.builder = builder or UmlModelBuilder()

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



