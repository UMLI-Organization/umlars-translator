from typing import Union, Optional

from kink import inject

from umlars_translator.core.model.abstract.uml_elements import IUmlClassifier
from umlars_translator.core.serialization.abstract.serializer import UmlSerializer
from umlars_translator.core.model.umlars_model.uml_diagrams import UmlDiagrams, UmlClassDiagram, UmlSequenceDiagram, UmlClassDiagramElements, UmlSequenceDiagramElements
from umlars_translator.core.model.umlars_model.uml_elements import (
    UmlElement,
    UmlClass,
    UmlAttribute,
    UmlDirectedAssociation,
    UmlAssociation,
    UmlAssociationEnd,
    UmlModelElements,
    UmlPrimitiveType,
    UmlInterface,
    UmlDataType,
    UmlEnumeration,
    UmlOperation,
    UmlParameter,
    UmlDependency,
    UmlRealization,
    UmlGeneralization,
    UmlMessage,
    UmlAggregation,
    UmlComposition,
    UmlInteraction,
    UmlLifeline,
    UmlCombinedFragment,
    UmlOperand,
    UmlInteractionUse,
    UmlOccurrenceSpecification,
    UmlPackage,
)
from umlars_translator.core.model.umlars_model.uml_model import UmlModel

import umlars_translator.app.dtos.uml_model as pydantic_uml


@inject(alias=UmlSerializer)
class UmlToPydanticSerializer(UmlSerializer):
    def serialize(self, model: UmlModel, to_string: bool = True) -> str:
        pydantic_model = self.visit_uml_model(model)
        
        if not to_string:
            return pydantic_model
        
        return pydantic_model.model_dump_json()

    def visit_uml_model(self, model: UmlModel) -> pydantic_uml.UmlModel:
        return pydantic_uml.UmlModel(
            id=model.id,
            name=model.name,
            elements=self.visit_uml_model_elements(model.elements),
            diagrams=self.visit_uml_diagrams(model.diagrams),
            metadata=model.metadata,
        )

    def visit_uml_model_elements(self, elements: UmlModelElements) -> pydantic_uml.UmlModelElements:
        return pydantic_uml.UmlModelElements(
            classes=[self.visit_uml_class(cls) for cls in elements.classes],
            interfaces=[self.visit_uml_interface(interface) for interface in elements.interfaces],
            data_types=[self.visit_uml_data_type(data_type) for data_type in elements.data_types],
            enumerations=[self.visit_uml_enumeration(enum) for enum in elements.enumerations],
            primitive_types=[self.visit_uml_primitive_type(primitive) for primitive in elements.primitive_types],
            associations=[self.visit_uml_association(assoc) for assoc in elements.associations],
            generalizations=[self.visit_uml_generalization(gen) for gen in elements.generalizations],
            dependencies=[self.visit_uml_dependency(dep) for dep in elements.dependencies],
            realizations=[self.visit_uml_realization(real) for real in elements.realizations],
            interactions=[self.visit_uml_interaction(interaction) for interaction in elements.interactions],
            packages=[self.visit_uml_package(package) for package in elements.packages],
        )

    def visit_uml_class(self, uml_class: UmlClass) -> pydantic_uml.UmlClass:
        return pydantic_uml.UmlClass(
            id=uml_class.id,
            name=uml_class.name,
            visibility=uml_class.visibility,
            attributes=[self.visit_uml_attribute(attr) for attr in uml_class.attributes],
            operations=[self.visit_uml_operation(op) for op in uml_class.operations],
            generalizations=[self.visit_uml_generalization(gen) for gen in uml_class.generalizations],
            interfaces=[self.visit_uml_realization(real) for real in uml_class.interfaces],
        )

    def visit_uml_interface(self, uml_interface: UmlInterface) -> pydantic_uml.UmlInterface:
        return pydantic_uml.UmlInterface(
            id=uml_interface.id,
            name=uml_interface.name,
            visibility=uml_interface.visibility,
            attributes=[self.visit_uml_attribute(attr) for attr in uml_interface.attributes],
            operations=[self.visit_uml_operation(op) for op in uml_interface.operations],
        )

    def visit_uml_attribute(self, attribute: UmlAttribute) -> pydantic_uml.UmlAttribute:
        return pydantic_uml.UmlAttribute(
            id=attribute.id,
            name=attribute.name,
            visibility=attribute.visibility,
            type=self.visit_element_or_reference(attribute.type),
            is_static=attribute.is_static,
            is_ordered=attribute.is_ordered,
            is_unique=attribute.is_unique,
            is_read_only=attribute.is_read_only,
            is_query=attribute.is_query,
            is_derived=attribute.is_derived,
            is_derived_union=attribute.is_derived_union,
        )

    def visit_uml_operation(self, operation: UmlOperation) -> pydantic_uml.UmlOperation:
        return pydantic_uml.UmlOperation(
            id=operation.id,
            name=operation.name,
            visibility=operation.visibility,
            return_type=self.visit_element_or_reference(operation.return_type),
            parameters=[self.visit_uml_parameter(param) for param in operation.parameters],
            is_static=operation.is_static,
            is_ordered=operation.is_ordered,
            is_unique=operation.is_unique,
            is_query=operation.is_query,
            is_derived=operation.is_derived,
            is_derived_union=operation.is_derived_union,
            is_abstract=operation.is_abstract,
            exceptions=operation.exceptions,
        )

    def visit_uml_parameter(self, parameter: UmlParameter) -> pydantic_uml.UmlParameter:
        return pydantic_uml.UmlParameter(
            id=parameter.id,
            name=parameter.name,
            visibility=parameter.visibility,
            type=self.visit_element_or_reference(parameter.type),
            direction=parameter.direction,
        )

    def visit_uml_aggregation(
        self, element: UmlAggregation
    ) -> pydantic_uml.UmlAggregation:
        return pydantic_uml.UmlAggregation(
            id=element.id,
            name=element.name,
            visibility=element.visibility,
            source=self.visit_uml_association_end(element.source),
            target=self.visit_uml_association_end(element.target),
            type=element.type,
            direction=element.direction,
        )

    def visit_uml_composition(
        self, element: UmlComposition
    ) -> pydantic_uml.UmlComposition:
        return pydantic_uml.UmlComposition(
            id=element.id,
            name=element.name,
            visibility=element.visibility,
            source=self.visit_uml_association_end(element.source),
            target=self.visit_uml_association_end(element.target),
            type=element.type,
            direction=element.direction,
        )

    def visit_uml_association(self, association: UmlAssociation) -> pydantic_uml.UmlAssociation:
        if isinstance(association, UmlAggregation):
            return self.visit_uml_aggregation(association)
        elif isinstance(association, UmlComposition):
            return self.visit_uml_composition(association)
        elif isinstance(association, UmlAssociation):
            return pydantic_uml.UmlAssociation(
                id=association.id,
                name=association.name,
                visibility=association.visibility,
                end1=self.visit_uml_association_end(association.end1),
                end2=self.visit_uml_association_end(association.end2),
                type=association.type,
                direction=association.direction,
            )
        else:
            raise ValueError("Unsupported association type")

    def visit_uml_association_end(self, association_end: UmlAssociationEnd) -> pydantic_uml.UmlAssociationEnd:
        if association_end is None:
            return None
        
        return pydantic_uml.UmlAssociationEnd(
            id=association_end.id,
            multiplicity=association_end.multiplicity,
            element=self.visit_element_or_reference(association_end.element),
            role=association_end.role,
            navigability=association_end.navigability,
        )

    def visit_uml_dependency(self, dependency: UmlDependency) -> pydantic_uml.UmlDependency:
        return pydantic_uml.UmlDependency(
            id=dependency.id,
            supplier=self.visit_element_or_reference(dependency.supplier),
            client=self.visit_element_or_reference(dependency.client),
        )

    def visit_uml_realization(self, realization: UmlRealization) -> pydantic_uml.UmlRealization:
        return pydantic_uml.UmlRealization(
            id=realization.id,
            supplier=self.visit_element_or_reference(realization.supplier),
            client=self.visit_element_or_reference(realization.client),
        )

    def visit_uml_generalization(self, generalization: UmlGeneralization) -> pydantic_uml.UmlGeneralization:
        return pydantic_uml.UmlGeneralization(
            id=generalization.id,
            specific=self.visit_element_or_reference(generalization.specific),
            general=self.visit_element_or_reference(generalization.general),
        )

    def visit_uml_primitive_type(self, primitive_type: UmlPrimitiveType) -> pydantic_uml.UmlPrimitiveType:
        return pydantic_uml.UmlPrimitiveType(
            id=primitive_type.id,
            name=primitive_type.name,
            visibility=primitive_type.visibility,
            kind=primitive_type.kind,
        )

    def visit_uml_data_type(self, data_type: UmlDataType) -> pydantic_uml.UmlDataType:
        return pydantic_uml.UmlDataType(
            id=data_type.id,
            name=data_type.name,
            visibility=data_type.visibility,
        )

    def visit_uml_enumeration(self, enumeration: UmlEnumeration) -> pydantic_uml.UmlEnumeration:
        return pydantic_uml.UmlEnumeration(
            id=enumeration.id,
            name=enumeration.name,
            visibility=enumeration.visibility,
            literals=enumeration.literals,
        )

    def visit_uml_message(self, message: UmlMessage) -> pydantic_uml.UmlMessage:
        return pydantic_uml.UmlMessage(
            id=message.id,
            name=message.name,
            visibility=message.visibility,
            send_event=self.visit_element_or_reference(message.send_event),
            receive_event=self.visit_element_or_reference(message.receive_event),
            signature=self.visit_element_or_reference(message.signature),
            arguments=message.arguments,
            sort=message.sort,
            kind=message.kind,
        )

    def visit_uml_interaction(self, interaction: UmlInteraction) -> pydantic_uml.UmlInteraction:
        return pydantic_uml.UmlInteraction(
            id=interaction.id,
            name=interaction.name,
            visibility=interaction.visibility,
            lifelines=[self.visit_uml_lifeline(ll) for ll in interaction.lifelines],
            messages=[self.visit_uml_message(msg) for msg in interaction.messages],
            fragments=[self.visit_uml_fragment(frag) for frag in interaction.fragments],
        )

    def visit_uml_lifeline(self, lifeline: UmlLifeline) -> pydantic_uml.UmlLifeline:
        return pydantic_uml.UmlLifeline(
            id=lifeline.id,
            name=lifeline.name,
            visibility=lifeline.visibility,
            represents=self.visit_element_or_reference(lifeline.represents),
        )

    def visit_uml_occurrence_specification(
        self, occurrence_spec: UmlOccurrenceSpecification
    ) -> pydantic_uml.UmlOccurrenceSpecification:
        return pydantic_uml.UmlOccurrenceSpecification(
            id=occurrence_spec.id,
            covered=self.visit_element_or_reference(occurrence_spec.covered),
        )

    def visit_uml_combined_fragment(
        self, combined_fragment: UmlCombinedFragment
    ) -> pydantic_uml.UmlCombinedFragment:
        return pydantic_uml.UmlCombinedFragment(
            id=combined_fragment.id,
            name=combined_fragment.name,
            visibility=combined_fragment.visibility,
            operator=combined_fragment.operator,
            covered=[
                self.visit_element_or_reference(covered)
                for covered in combined_fragment.covered
            ],
            operands=[self.visit_uml_operand(operand) for operand in combined_fragment.operands],
        )

    def visit_uml_operand(self, operand: UmlOperand) -> pydantic_uml.UmlOperand:
        return pydantic_uml.UmlOperand(
            id=operand.id,
            guard=operand.guard,
            fragments=[
                self.visit_uml_fragment(fragment) for fragment in operand.fragments
            ],
        )

    def visit_uml_interaction_use(self, interaction_use: UmlInteractionUse) -> pydantic_uml.UmlInteractionUse:
        return pydantic_uml.UmlInteractionUse(
            id=interaction_use.id,
            name=interaction_use.name,
            visibility=interaction_use.visibility,
            interaction=self.visit_element_or_reference(interaction_use.interaction),
            covered=[
                self.visit_element_or_reference(covered)
                for covered in interaction_use.covered
            ],
        )

    def visit_uml_package(self, uml_package: UmlPackage) -> pydantic_uml.UmlPackage:
        return pydantic_uml.UmlPackage(
            id=uml_package.id,
            name=uml_package.name,
            visibility=uml_package.visibility,
            elements=self.visit_element_or_reference(uml_package.elements),
        )

    def visit_element_or_reference(self, element: Optional[UmlElement] = None) -> Union[pydantic_uml.UmlElement, pydantic_uml.UmlIdReference]:
        if isinstance(element, UmlElement):
            return pydantic_uml.UmlIdReference(idref=element.id)
        elif element is None:
            return None
        else:
            raise ValueError("Unsupported element type")

    def visit_uml_diagrams(self, diagrams: UmlDiagrams) -> pydantic_uml.UmlDiagrams:
        return pydantic_uml.UmlDiagrams(
            class_diagrams=[self.visit_uml_class_diagram(diag) for diag in diagrams.class_diagrams],
            sequence_diagrams=[self.visit_uml_sequence_diagram(diag) for diag in diagrams.sequence_diagrams],
        )

    def visit_uml_class_diagram(self, class_diagram: UmlClassDiagram) -> pydantic_uml.UmlClassDiagram:
        return pydantic_uml.UmlClassDiagram(
            id=class_diagram.id,
            name=class_diagram.name,
            description=class_diagram.description,
            elements=self.visit_uml_class_diagram_elements(class_diagram.elements),
        )

    def visit_uml_class_diagram_elements(
        self, elements: UmlClassDiagramElements
    ) -> pydantic_uml.UmlClassDiagramElements:
        return pydantic_uml.UmlClassDiagramElements(
            classes=[self.visit_element_or_reference(cls) for cls in elements.classes],
            interfaces=[self.visit_element_or_reference(interface) for interface in elements.interfaces],
            data_types=[self.visit_element_or_reference(data_type) for data_type in elements.data_types],
            enumerations=[self.visit_element_or_reference(enum) for enum in elements.enumerations],
            primitive_types=[self.visit_element_or_reference(primitive) for primitive in elements.primitive_types],
            associations=[self.visit_element_or_reference(assoc) for assoc in elements.associations],
            generalizations=[self.visit_element_or_reference(gen) for gen in elements.generalizations],
            dependencies=[self.visit_element_or_reference(dep) for dep in elements.dependencies],
            realizations=[self.visit_element_or_reference(real) for real in elements.realizations],
        )

    def visit_uml_sequence_diagram(self, sequence_diagram: UmlSequenceDiagram) -> pydantic_uml.UmlSequenceDiagram:
        return pydantic_uml.UmlSequenceDiagram(
            id=sequence_diagram.id,
            name=sequence_diagram.name,
            description=sequence_diagram.description,
            elements=self.visit_uml_sequence_diagram_elements(sequence_diagram.elements),
        )

    def visit_uml_sequence_diagram_elements(
        self, elements: UmlSequenceDiagramElements
    ) -> pydantic_uml.UmlSequenceDiagramElements:
        return pydantic_uml.UmlSequenceDiagramElements(
            interactions=[self.visit_element_or_reference(interaction) for interaction in elements.interactions],
        )

    def visit_uml_fragment(
        self, fragment: Union[UmlOccurrenceSpecification, UmlCombinedFragment, UmlInteractionUse]
    ) -> Union[pydantic_uml.UmlOccurrenceSpecification, pydantic_uml.UmlCombinedFragment, pydantic_uml.UmlInteractionUse]:
        if isinstance(fragment, UmlOccurrenceSpecification):
            return self.visit_uml_occurrence_specification(fragment)
        elif isinstance(fragment, UmlCombinedFragment):
            return self.visit_uml_combined_fragment(fragment)
        elif isinstance(fragment, UmlInteractionUse):
            return self.visit_uml_interaction_use(fragment)
        else:
            raise ValueError("Unsupported fragment type")

    # Empty implementations for basic elements and directed association
    def visit_uml_element(self, element: UmlElement) -> None:
        pass

    def visit_uml_named_element(
        self, element: UmlElement
    ) -> None:
        pass

    def visit_uml_directed_association(
        self, element: UmlDirectedAssociation
    ) -> None:
        pass

    def visit_uml_classifier(self, classifier: IUmlClassifier) -> None:
        pass