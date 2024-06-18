from kink import di

from umlars_translator.core.model.umlars_model.umlars_uml_model_builder import (
    UmlModelBuilder,
)
from umlars_translator.core.model.abstract.uml_model_builder import IUmlModelBuilder


# TODO: for now if wanted to change the builder, it needs to be done here.
# If it becomes a common case factory pattern can be used similarly to the deserialization factory.
def bootstrap_di() -> None:
    model_builder = UmlModelBuilder()

    di[UmlModelBuilder] = model_builder
    di[IUmlModelBuilder] = model_builder
