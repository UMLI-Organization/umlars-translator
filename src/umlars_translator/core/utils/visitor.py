from typing import Any, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from umlars_translator.core.model.abstract.uml_elements import IUmlElement, IUmlNamedElement, IUmlPrimitiveType, IUmlClassifier, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration, IUmlAttribute, IUmlOperation, IUmlParameter, IUmlGeneralization, IUmlDependency, IUmlRealization, IUmlAssociationEnd, IUmlAssociation, IUmlDirectedAssociation, IUmlAggregation, IUmlComposition, IUmlOccurrenceSpecification, IUmlInteractionUse, IUmlCombinedFragment, IUmlOperand, IUmlLifeline, IUmlMessage, IUmlInteraction, IUmlModelElements, IUmlPackage, IUmlModel
    from umlars_translator.core.model.abstract.uml_diagrams import IUmlDiagrams, IUmlClassDiagram, IUmlSequenceDiagram, IUmlClassDiagramElements, IUmlSequenceDiagramElements


class IVisitor(ABC):
    ...


class IModelVisitor(ABC):
    """
    Visitor interface for UML elements.
    """

    @abstractmethod
    def visit_uml_element(self, element: 'IUmlElement') -> Any:
        ...

    @abstractmethod
    def visit_uml_named_element(self, element: 'IUmlNamedElement') -> Any:
        ...

    @abstractmethod
    def visit_uml_primitive_type(self, primitive_type: 'IUmlPrimitiveType') -> Any:
        ...

    @abstractmethod
    def visit_uml_classifier(self, classifier: 'IUmlClassifier') -> Any:
        ...

    @abstractmethod
    def visit_uml_class(self, uml_class: 'IUmlClass') -> Any:
        ...

    @abstractmethod
    def visit_uml_interface(self, uml_interface: 'IUmlInterface') -> Any:
        ...

    @abstractmethod
    def visit_uml_data_type(self, data_type: 'IUmlDataType') -> Any:
        ...

    @abstractmethod
    def visit_uml_enumeration(self, enumeration: 'IUmlEnumeration') -> Any:
        ...

    @abstractmethod
    def visit_uml_attribute(self, attribute: 'IUmlAttribute') -> Any:
        ...

    @abstractmethod
    def visit_uml_operation(self, operation: 'IUmlOperation') -> Any:
        ...

    @abstractmethod
    def visit_uml_parameter(self, parameter: 'IUmlParameter') -> Any:
        ...

    @abstractmethod
    def visit_uml_generalization(self, generalization: 'IUmlGeneralization') -> Any:
        ...

    @abstractmethod
    def visit_uml_dependency(self, dependency: 'IUmlDependency') -> Any:
        ...

    @abstractmethod
    def visit_uml_realization(self, realization: 'IUmlRealization') -> Any:
        ...

    @abstractmethod
    def visit_uml_association_end(self, association_end: 'IUmlAssociationEnd') -> Any:
        ...

    @abstractmethod
    def visit_uml_association(self, association: 'IUmlAssociation') -> Any:
        ...

    @abstractmethod
    def visit_uml_directed_association(self, directed_association: 'IUmlDirectedAssociation') -> Any:
        ...

    @abstractmethod
    def visit_uml_aggregation(self, aggregation: 'IUmlAggregation') -> Any:
        ...

    @abstractmethod
    def visit_uml_composition(self, composition: 'IUmlComposition') -> Any:
        ...

    @abstractmethod
    def visit_uml_occurrence_specification(self, occurrence_specification: 'IUmlOccurrenceSpecification') -> Any:
        ...

    @abstractmethod
    def visit_uml_interaction_use(self, interaction_use: 'IUmlInteractionUse') -> Any:
        ...

    @abstractmethod
    def visit_uml_combined_fragment(self, combined_fragment: 'IUmlCombinedFragment') -> Any:
        ...

    @abstractmethod
    def visit_uml_operand(self, operand: 'IUmlOperand') -> Any:
        ...

    @abstractmethod
    def visit_uml_lifeline(self, lifeline: 'IUmlLifeline') -> Any:
        ...

    @abstractmethod
    def visit_uml_message(self, message: 'IUmlMessage') -> Any:
        ...

    @abstractmethod
    def visit_uml_interaction(self, interaction: 'IUmlInteraction') -> Any:
        ...

    @abstractmethod
    def visit_uml_model_elements(self, model_elements: 'IUmlModelElements') -> Any:
        ...

    @abstractmethod
    def visit_uml_package(self, uml_package: 'IUmlPackage') -> Any:
        ...

    @abstractmethod
    def visit_uml_class_diagram_elements(self, class_diagram_elements: 'IUmlClassDiagramElements') -> Any:
        ...

    @abstractmethod
    def visit_uml_sequence_diagram_elements(self, sequence_diagram_elements: 'IUmlSequenceDiagramElements') -> Any:
        ...

    @abstractmethod
    def visit_uml_class_diagram(self, class_diagram: 'IUmlClassDiagram') -> Any:
        ...

    @abstractmethod
    def visit_uml_sequence_diagram(self, sequence_diagram: 'IUmlSequenceDiagram') -> Any:
        ...

    @abstractmethod
    def visit_uml_diagrams(self, uml_diagrams: 'IUmlDiagrams') -> Any:
        ...

    @abstractmethod
    def visit_uml_model(self, uml_model: 'IUmlModel') -> Any:
        ...


class IVisitable(ABC):
    @abstractmethod
    def accept(self, visitor: IVisitor):
        pass
