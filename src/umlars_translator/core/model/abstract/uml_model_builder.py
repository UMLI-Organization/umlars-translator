from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Union, List
from functools import wraps
from logging import Logger
import logging

from kink import inject

from umlars_translator.core.model.abstract.uml_model import IUmlModel
from umlars_translator.core.model.constants import UmlVisibilityEnum, UmlMultiplicityEnum, UmlPrimitiveTypeKindEnum, UmlParameterDirectionEnum, UmlInteractionOperatorEnum, UmlMessageSortEnum, UmlMessageKindEnum


def log_calls_and_return_self(log_level: int = logging.DEBUG) -> Callable:
    def inner(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self, *args, **kwargs) -> Any:
            self._logger.log(
                log_level, f"Method called: {method.__name__}({args}, {kwargs})"
            )
            return self

        return wrapper

    return inner


@inject
class IUmlModelBuilder(ABC):
    """
    Interface required by the final UmlBuilder implementation.
    Main requirement for a subclass is to provide methods `build` and `clear`.
    If other methods are not implemented, calling them won't disrupt the process and the call wll just be logged.
    """
    _logger: Logger
    _model: IUmlModel

    @property
    def model(self) -> IUmlModel:
        return self._model
    
    @model.setter
    def model(self, new_model: IUmlModel) -> None:
        self._model = new_model

    @abstractmethod
    def build(self) -> IUmlModel:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...

    # Base Methods
    @log_calls_and_return_self()
    def bind_element_to_diagram(self, *args, **kwargs) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_diagram(self, *args, **kwargs) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_metadata(self, *args, **kwargs) -> "IUmlModelBuilder":
        ...

    # UML Element Methods
    @log_calls_and_return_self()
    def construct_uml_element(self, id: str, name: Optional[str] = None) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_named_element(self, id: str, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC) -> "IUmlModelBuilder":
        ...

    # Primitive Types
    @log_calls_and_return_self()
    def construct_uml_primitive_type(self, name: Optional[str] = None, kind: UmlPrimitiveTypeKindEnum = UmlPrimitiveTypeKindEnum.STRING) -> "IUmlModelBuilder":
        ...

    # Classifiers
    @log_calls_and_return_self()
    def construct_uml_classifier(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, attributes: Optional[List['IUmlAttribute']] = None, operations: Optional[List['IUmlOperation']] = None) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_class(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, generalizations: Optional[List['IUmlGeneralization']] = None, interfaces: Optional[List['IUmlInterface']] = None) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_interface(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_data_type(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_enumeration(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, literals: Optional[List[str]] = None) -> "IUmlModelBuilder":
        ...

    # Attributes and Operations
    @log_calls_and_return_self()
    def construct_uml_attribute(self, classifier_id: str, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, type: Union['IUmlPrimitiveType', 'IUmlClass', 'IUmlInterface', 'IUmlDataType', 'IUmlEnumeration'] = None, is_static: Optional[bool] = None, is_ordered: Optional[bool] = None, is_unique: Optional[bool] = None, is_read_only: Optional[bool] = None, is_query: Optional[bool] = None, is_derived: Optional[bool] = None, is_derived_union: Optional[bool] = None, type_metadata: Optional[dict[str, Any]] = None) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_operation(self, classifier_id: str, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, return_type: Optional[Union['IUmlPrimitiveType', 'IUmlClass', 'IUmlInterface', 'IUmlDataType', 'IUmlEnumeration']] = None, parameters: Optional[List['IUmlParameter']] = None, is_static: Optional[bool] = None, is_ordered: Optional[bool] = None, is_unique: Optional[bool] = None, is_query: Optional[bool] = None, is_derived: Optional[bool] = None, is_derived_union: Optional[bool] = None, is_abstract: bool = False, exceptions: Optional[List[str]] = None, type_metadata: Optional[dict[str, Any]] = None) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_parameter(self, name: Optional[str] = None, type: Union['IUmlPrimitiveType', 'IUmlClass', 'IUmlInterface', 'IUmlDataType', 'IUmlEnumeration'] = None, direction: UmlParameterDirectionEnum = UmlParameterDirectionEnum.IN) -> "IUmlModelBuilder":
        ...

    # Relationships
    @log_calls_and_return_self()
    def construct_uml_generalization(self, specific: 'IUmlClass', general: 'IUmlClass') -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_dependency(self, client: 'IUmlClassifier', supplier: 'IUmlClassifier') -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_realization(self, client: 'IUmlClassifier', supplier: 'IUmlClassifier') -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_association_end(self, element: 'IUmlClassifier', role: Optional[str] = None, multiplicity: UmlMultiplicityEnum = UmlMultiplicityEnum.ONE, navigability: bool = True) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_association(self, end1: 'IUmlAssociationEnd', end2: 'IUmlAssociationEnd') -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_directed_association(self, source: 'IUmlAssociationEnd', target: 'IUmlAssociationEnd') -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_aggregation(self, source: 'IUmlAssociationEnd', target: 'IUmlAssociationEnd') -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_composition(self, source: 'IUmlAssociationEnd', target: 'IUmlAssociationEnd') -> "IUmlModelBuilder":
        ...

    # Interaction Elements
    @log_calls_and_return_self()
    def construct_uml_occurrence_specification(self, covered: 'IUmlLifeline') -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_interaction_use(self, covered: Optional[List['IUmlLifeline']] = None, interaction: Optional['IUmlInteraction'] = None) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_combined_fragment(self, operands: Optional[List['IUmlOperand']] = None, covered: Optional[List['IUmlLifeline']] = None, operator: UmlInteractionOperatorEnum = UmlInteractionOperatorEnum.ALT) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_operand(self, guard: Optional[str] = None, fragments: Optional[List[Union['IUmlOccurrenceSpecification', 'IUmlInteractionUse', 'IUmlCombinedFragment']]] = None) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_lifeline(self, name: Optional[str] = None, represents: Optional[Union['IUmlClass', 'IUmlInterface']] = None) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_message(self, send_event: 'IUmlOccurrenceSpecification', receive_event: 'IUmlOccurrenceSpecification', signature: Optional['IUmlOperation'] = None, arguments: Optional[List[str]] = None, sort: UmlMessageSortEnum = UmlMessageSortEnum.SYNCH_CALL, kind: UmlMessageKindEnum = UmlMessageKindEnum.COMPLETE) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_interaction(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, lifelines: Optional[List['IUmlLifeline']] = None, messages: Optional[List['IUmlMessage']] = None, fragments: Optional[List[Union['IUmlOccurrenceSpecification', 'IUmlInteractionUse', 'IUmlCombinedFragment']]] = None) -> "IUmlModelBuilder":
        ...

    # Model and Package Elements
    @log_calls_and_return_self()
    def construct_uml_model_elements(self, classes: Optional[List['IUmlClass']] = None, interfaces: Optional[List['IUmlInterface']] = None, data_types: Optional[List['IUmlDataType']] = None, enumerations: Optional[List['IUmlEnumeration']] = None, primitive_types: Optional[List['IUmlPrimitiveType']] = None, associations: Optional[List[Union['IUmlAssociation', 'IUmlDirectedAssociation']]] = None, generalizations: Optional[List['IUmlGeneralization']] = None, dependencies: Optional[List['IUmlDependency']] = None, realizations: Optional[List['IUmlRealization']] = None, interactions: Optional[List['IUmlInteraction']] = None, packages: Optional[List['IUmlPackage']] = None) -> "IUmlModelBuilder":
        ...

    @log_calls_and_return_self()
    def construct_uml_package(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, elements: Optional['IUmlModelElements'] = None) -> "IUmlModelBuilder":
        ...
