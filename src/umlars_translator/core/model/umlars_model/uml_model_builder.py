from typing import Any, Optional, List, Union
from logging import Logger

from kink import inject

from umlars_translator.core.model.abstract.uml_model_builder import IUmlModelBuilder
from umlars_translator.core.model.umlars_model.uml_model import UmlModel
from umlars_translator.core.model.umlars_model.uml_elements import (
    UmlElement, UmlClass, UmlLifeline, UmlAssociationEnd, UmlAssociationBase, UmlVisibilityEnum, UmlInterface,
    UmlPackage, UmlPrimitiveType, UmlAttribute, UmlOperation, UmlLifeline, UmlAssociationEnd, UmlAssociationBase,
    UmlAggregation, UmlComposition, UmlRealization, UmlGeneralization, UmlDependency, UmlDirectedAssociation,
    UmlAssociation, UmlDataType, UmlEnumeration, UmlParameter, UmlMessage, UmlInteraction, UmlOccurrenceSpecification,
    UmlInteractionUse, UmlCombinedFragment, UmlOperand, UmlClassifier
)
from umlars_translator.core.utils.delayed_caller import (
    DalayedIdToInstanceMapper,
    evaluate_elements_afterwards,
)
from umlars_translator.core.model.umlars_model.uml_diagrams import UmlDiagram, UmlClassDiagram, UmlSequenceDiagram
from umlars_translator.core.model.constants import UmlVisibilityEnum, UmlMultiplicityEnum, UmlPrimitiveTypeKindEnum, UmlParameterDirectionEnum, UmlInteractionOperatorEnum, UmlMessageSortEnum, UmlMessageKindEnum


@inject
class UmlModelBuilder(DalayedIdToInstanceMapper, IUmlModelBuilder):
    def __init__(
        self, model: Optional[UmlModel] = None, core_logger: Optional[Logger] = None
    ) -> None:
        self._logger = core_logger.getChild(self.__class__.__name__)
        super().__init__(core_logger=self._logger)

        self._model = model if model is not None else UmlModel(builder=self)

    def build(self) -> UmlModel:
        self._evaluate_queues()
        return self._model

    def clear(self) -> None:
        self._model = UmlModel(builder=self)
        super().clear()

    def add_element(self, element: Any) -> 'IUmlModelBuilder':
        self.register_if_not_present(element)
        return self

    def construct_uml_model(self, name: Optional[str] = None, visibility: Optional[UmlVisibilityEnum] = UmlVisibilityEnum.PUBLIC, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_model({args}, {kwargs})")
        self._model.name = name
        self._model.visibility = visibility
        return self

    def bind_element_to_diagram(self, element: Optional[UmlElement] = None, element_id: Optional[str] = None, diagram: Optional[UmlDiagram] = None, diagram_id: Optional[str] = None,  *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: bind_element_to_diagram({args}, {kwargs})")
        element = element if element is not None else self.get_instance_by_id(element_id)
        diagram = diagram if diagram is not None else self.get_instance_by_id(diagram_id)

        if element is None:
            self._bind_not_initialized_element_to_diagram(element_id, diagram, diagram_id)
        else:
            self._bind_initialized_element_to_diagram(element, diagram, diagram_id)

        return self

    def construct_metadata(self, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_metadata({args}, {kwargs})")
        self.model.metadata = kwargs
        return self

    # Classifiers
    def construct_uml_class(self, id: Optional[str] = None, name: Optional[str] = None, visibility: Optional[UmlVisibilityEnum] = UmlVisibilityEnum.PUBLIC, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_class({args}, {kwargs})")
        uml_class = UmlClass(id=id, name=name, visibility=visibility, model=self._model, builder=self)
        self.add_class(uml_class)
        return self
    
    def add_class(self, uml_class: UmlClass) -> "IUmlModelBuilder":
        self.add_element(uml_class)
        self.model.elements.classes.append(uml_class)
        return self

    def construct_uml_interface(self, id: Optional[str] = None, name: Optional[str] = None, visibility: Optional[UmlVisibilityEnum] = UmlVisibilityEnum.PUBLIC, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_interface({args}, {kwargs})")
        uml_interface = UmlInterface(id=id, name=name, visibility=visibility, model=self._model, builder=self)
        self.add_interface(uml_interface)
        return self

    def add_interface(self, uml_interface: UmlInterface) -> "IUmlModelBuilder":
        self.add_element(uml_interface)
        self.model.elements.interfaces.append(uml_interface)
        return self

    def construct_uml_data_type(self, id: Optional[str] = None, name: Optional[str] = None, visibility: Optional[UmlVisibilityEnum] = UmlVisibilityEnum.PUBLIC, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_data_type({args}, {kwargs})")
        data_type = UmlDataType(id=id, name=name, visibility=visibility, model=self._model, builder=self)
        self.add_element(data_type)
        self.model.elements.data_types.append(data_type)
        return self

    def construct_uml_enumeration(self, id: Optional[str] = None, name: Optional[str] = None, visibility: Optional[UmlVisibilityEnum] = UmlVisibilityEnum.PUBLIC, literals: Optional[List[str]] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_enumeration({args}, {kwargs})")
        enumeration = UmlEnumeration(id=id, name=name, visibility=visibility, literals=literals or [], model=self._model, builder=self)
        self.add_element(enumeration)
        self.model.elements.enumerations.append(enumeration)
        return self

    def construct_uml_primitive_type(self, id: Optional[str] = None, name: Optional[str] = None, kind: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_primitive_type({args}, {kwargs})")
        primitive_type = UmlPrimitiveType(id=id, name=name, kind=kind, model=self._model, builder=self)
        self.add_element(primitive_type)
        self.model.elements.primitive_types.append(primitive_type)
        return self

    def construct_uml_attribute(self, classifier_id: str, id: Optional[str] = None, name: Optional[str] = None, visibility: Optional[UmlVisibilityEnum] = UmlVisibilityEnum.PUBLIC, type_id: Optional[str] = None, is_static: Optional[bool] = None, is_ordered: Optional[bool] = None, is_unique: Optional[bool] = None, is_read_only: Optional[bool] = None, is_query: Optional[bool] = None, is_derived: Optional[bool] = None, is_derived_union: Optional[bool] = None, type_metadata: Optional[dict[str, Any]]=None, **kwargs) -> "IUmlModelBuilder":
        if type_id is None:
            type_id = type_metadata.get('referenced_type_id') if type_metadata is not None else None
        self._logger.debug(f"Method called: construct_uml_attribute( {kwargs})")
        uml_type = self.get_instance_by_id(type_id)
        uml_class = self.get_instance_by_id(classifier_id)
        attribute = UmlAttribute(
            id=id, name=name, visibility=visibility, type=uml_type, is_static=is_static, is_ordered=is_ordered,
            is_unique=is_unique, is_read_only=is_read_only, is_query=is_query, is_derived=is_derived,
            is_derived_union=is_derived_union, model=self._model, builder=self
        )

        self.add_element(attribute)

        if uml_class is not None:
            uml_class.attributes.append(attribute)
        else:
            def _queued_assign_attribute(classifier: UmlClassifier) -> None:
                classifier.attributes.append(attribute)
            
            self.register_dalayed_call_for_id(classifier_id, _queued_assign_attribute)

        if uml_type is None:
            def _queued_assign_type(type: UmlElement) -> None:
                attribute.type = type
            
            self.register_dalayed_call_for_id(type_id, _queued_assign_type)

        return self
        
    def add_attribute(self, attribute: UmlAttribute) -> "IUmlModelBuilder":
        self.add_element(attribute)
        return self

    def construct_uml_operation(self, classifier_id: str, id: Optional[str] = None, name: Optional[str] = None, visibility: Optional[UmlVisibilityEnum] = UmlVisibilityEnum.PUBLIC, return_type_id: Optional[str] = None, type_metadata: Optional[dict[str, Any]] = None, **kwargs) -> "IUmlModelBuilder":
        if return_type_id is None:
            return_type_id = type_metadata.get('referenced_type_id') if type_metadata is not None else None
        self._logger.debug(f"Method called: construct_uml_operation({kwargs})")
        uml_class = self.get_instance_by_id(classifier_id)
        return_type = self.get_instance_by_id(return_type_id)
        operation = UmlOperation(
            id=id, name=name, visibility=visibility, return_type=return_type, model=self._model, builder=self
        )

        self.add_element(operation)

        if uml_class is not None:
            uml_class.operations.append(operation)
        else:
            def _queued_assign_operation(classifier: UmlClassifier) -> None:
                classifier.operations.append(operation)
            
            self.register_dalayed_call_for_id(classifier_id, _queued_assign_operation)

        if return_type is None:
            def _queued_assign_return_type(type: UmlElement) -> None:
                operation.return_type = type
            
            self.register_dalayed_call_for_id(return_type_id, _queued_assign_return_type)

        return self

        
    def add_operation(self, operation: UmlOperation) -> "IUmlModelBuilder":
        self.add_element(operation)
        return self

    def construct_uml_package(self, id: Optional[str] = None, name: Optional[str] = None, visibility: Optional[UmlVisibilityEnum] = UmlVisibilityEnum.PUBLIC, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_package({args}, {kwargs})")
        package = UmlPackage(id=id, name=name, visibility=visibility, model=self._model, builder=self)
        self.add_package(package)
        return self
    
    def add_package(self, package: UmlPackage) -> "IUmlModelBuilder":
        self.add_element(package)
        self.model.elements.packages.append(package)
        return self

    def add_class_to_package(self, class_id: str, package_id: str) -> "IUmlModelBuilder":
        uml_class = self.get_instance_by_id(class_id)
        package = self.get_instance_by_id(package_id)
        package.add_class(uml_class)
        return self

    def add_interface_to_package(self, interface_id: str, package_id: str) -> "IUmlModelBuilder":
        uml_interface = self.get_instance_by_id(interface_id)
        package = self.get_instance_by_id(package_id)
        package.add_interface(uml_interface)
        return self

    def add_association_to_package(self, association_id: str, package_id: str) -> "IUmlModelBuilder":
        uml_association = self.get_instance_by_id(association_id)
        package = self.get_instance_by_id(package_id)
        package.add_association(uml_association)
        return self
    
    def add_data_type_to_package(self, data_type_id: str, package_id: str) -> "IUmlModelBuilder":
        data_type = self.get_instance_by_id(data_type_id)
        package = self.get_instance_by_id(package_id)
        package.add_data_type(data_type)
        return self
    
    def add_enumeration_to_package(self, enumeration_id: str, package_id: str) -> "IUmlModelBuilder":
        enumeration = self.get_instance_by_id(enumeration_id)
        package = self.get_instance_by_id(package_id)
        package.add_enumeration(enumeration)
        return self    

    def construct_uml_lifeline(self, id: Optional[str] = None, name: Optional[str] = None, represents_id: Optional[str] = None, interaction_id: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_lifeline({args}, {kwargs})")
        represents = self.get_instance_by_id(represents_id)
        lifeline = UmlLifeline(id=id, name=name, represents=represents, model=self._model, builder=self)
        interaction = self.get_instance_by_id(interaction_id)
        self.add_lifeline(lifeline)

        if represents is None:
            def _queued_assign_represents(element: UmlElement) -> None:
                lifeline.represents = element
            
            self.register_dalayed_call_for_id(represents_id, _queued_assign_represents)

        if interaction is None:
            self.register_dalayed_call_for_id(interaction_id, lambda instance: instance.lifelines.append(lifeline))
        else:
            interaction.lifelines.append(lifeline)
        return self

    def add_lifeline(self, lifeline: UmlLifeline) -> "IUmlModelBuilder":
        self.add_element(lifeline)
        return self

    def construct_uml_association(self, id: Optional[str] = None, name: Optional[str] = None, end1_id: Optional[str] = None, end2_id: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_association({args}, {kwargs})")
        end1 = self.get_instance_by_id(end1_id)
        end2 = self.get_instance_by_id(end2_id)
        association = UmlAssociation(id=id, name=name, end1=end1, end2=end2, model=self._model, builder=self)
        self.add_association(association)

        if end1 is None:
            self.register_dalayed_call_for_id(end1_id, lambda e: setattr(association, 'end1', e))
        if end2 is None:
            self.register_dalayed_call_for_id(end2_id, lambda e: setattr(association, 'end2', e))

        return self

    def add_association(self, association: UmlAssociation) -> "IUmlModelBuilder":
        self.add_element(association)
        self.model.elements.associations.append(association)
        return self

    def construct_uml_association_end(
        self, 
        id: Optional[str] = None, 
        type_metadata: Optional[dict[str, Any]] = None,
        type_id: Optional[str] = None,
        role: Optional[str] = None, 
        multiplicity: Optional[UmlMultiplicityEnum] = UmlMultiplicityEnum.ONE, 
        navigability: bool = True, 
        association_id: Optional[str] = None,
        name: Optional[str] = None,
        visibility: Optional[UmlVisibilityEnum] = UmlVisibilityEnum.PUBLIC,
        *args, 
        **kwargs
    ) -> "IUmlModelBuilder":
        
        referenced_type_id = type_metadata.get('referenced_type_id') if type_metadata is not None else None
        if referenced_type_id is None:
            referenced_type_id = type_id
        
        self._logger.debug(f"Method called: construct_uml_association_end({args}, {kwargs})")
        element = self.get_instance_by_id(referenced_type_id)
        association = self.get_instance_by_id(association_id)

        association_end = UmlAssociationEnd(
            id=id, 
            element=element, 
            role=role, 
            multiplicity=multiplicity, 
            navigability=navigability, 
            name=name,
            visibility=visibility,
            model=self._model, 
            builder=self
        )
        
        # Bind to association if available or delay the assignment
        if association is not None:
            association.add_end(association_end)
        else:
            # Delayed assignment if the association is not available
            self.register_dalayed_call_for_id(association_id, lambda instance: instance.add_end(association_end))

        # Delayed assignment if the connected element is not available
        if element is None:
            def _queued_assign_element(element: UmlElement) -> None:
                association_end.element = element
            self.register_dalayed_call_for_id(referenced_type_id, lambda instance: _queued_assign_element(instance))

        return self

    # Relationships with Delayed Assignments
    def construct_uml_dependency(self, client_id: str, supplier_id: str, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_dependency({args}, {kwargs})")
        client = self.get_instance_by_id(client_id)
        supplier = self.get_instance_by_id(supplier_id)
        
        dependency = UmlDependency(client=client, supplier=supplier, model=self._model, builder=self)
        self.add_element(dependency)
        self.model.elements.dependencies.append(dependency)

        # Delayed assignment if client or supplier is not available
        if client is None:
            self.register_dalayed_call_for_id(client_id, lambda instance: setattr(dependency, 'client', instance))
        if supplier is None:
            self.register_dalayed_call_for_id(supplier_id, lambda instance: setattr(dependency, 'supplier', instance))

        return self

    def construct_uml_realization(self, client_id: str, supplier_id: str, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_realization({args}, {kwargs})")
        client = self.get_instance_by_id(client_id)
        supplier = self.get_instance_by_id(supplier_id)
        
        realization = UmlRealization(client=client, supplier=supplier, model=self._model, builder=self)
        self.add_element(realization)
        self.model.elements.realizations.append(realization)

        # Delayed assignment if client or supplier is not available
        if client is None:
            self.register_dalayed_call_for_id(client_id, lambda instance: setattr(realization, 'client', instance))

            def _queued_assign_supplier(instance: UmlElement) -> None:
                instance.interfaces.append(realization)

            self.register_dalayed_call_for_id(client_id, _queued_assign_supplier)
        else:
            client.interfaces.append(realization)

        if supplier is None:
            self.register_dalayed_call_for_id(supplier_id, lambda instance: setattr(realization, 'supplier', instance))

        return self

    def construct_uml_generalization(self, specific_id: str, general_id: str, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_generalization({args}, {kwargs})")
        specific = self.get_instance_by_id(specific_id)
        general = self.get_instance_by_id(general_id)
        
        generalization = UmlGeneralization(specific=specific, general=general, model=self._model, builder=self)
        self.add_element(generalization)
        self.model.elements.generalizations.append(generalization)

        # Delayed assignment if specific or general is not available
        if specific is None:
            self.register_dalayed_call_for_id(specific_id, lambda instance: setattr(generalization, 'specific', instance))

            def _queued_assign_general(instance: UmlElement) -> None:
                instance.generalizations.append(generalization)

            self.register_dalayed_call_for_id(specific_id, _queued_assign_general)
        
        else:
            specific.generalizations.append(generalization)

        if general is None:
            self.register_dalayed_call_for_id(general_id, lambda instance: setattr(generalization, 'general', instance))

        return self

    def construct_uml_aggregation(self, id: Optional[str] = None, source_id: str = None, target_id: str = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_aggregation({args}, {kwargs})")
        source = self.get_instance_by_id(source_id)
        target = self.get_instance_by_id(target_id)
        
        aggregation = UmlAggregation(id=id, source=source, target=target, model=self._model, builder=self)
        self.add_element(aggregation)
        self.model.elements.associations.append(aggregation)

        # Delayed assignment if source or target is not available
        if source is None:
            self.register_dalayed_call_for_id(source_id, lambda instance: setattr(aggregation, 'source', instance))
        if target is None:
            self.register_dalayed_call_for_id(target_id, lambda instance: setattr(aggregation, 'target', instance))

        return self

    def construct_uml_composition(self, id: Optional[str] = None, source_id: str = None, target_id: str = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_composition({args}, {kwargs})")
        source = self.get_instance_by_id(source_id)
        target = self.get_instance_by_id(target_id)
        
        composition = UmlComposition(id=id, source=source, target=target, model=self._model, builder=self)
        self.add_element(composition)
        self.model.elements.associations.append(composition)

        # Delayed assignment if source or target is not available
        if source is None:
            self.register_dalayed_call_for_id(source_id, lambda instance: setattr(composition, 'source', instance))
        if target is None:
            self.register_dalayed_call_for_id(target_id, lambda instance: setattr(composition, 'target', instance))

        return self

    def construct_uml_message(self, id: Optional[str] = None, name: Optional[str] = None, send_event_id: Optional[str] = None, receive_event_id: Optional[str] = None, source_lifeline_id: Optional[str] = None, target_lifeline_id: Optional[str] = None, message_sort: Optional[UmlMessageSortEnum] = UmlMessageSortEnum.SYNCH_CALL, kind: Optional[UmlMessageKindEnum] = UmlMessageKindEnum.UNKNOWN, signature_id: Optional[str] = None, create_new_occurences: bool = True, interaction_id: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_message({args}, {kwargs})")
        interaction = self.get_instance_by_id(interaction_id)

        if create_new_occurences and not (send_event_id and receive_event_id):
            self.construct_uml_occurrence_specification(covered_id=source_lifeline_id, interaction_id=interaction_id)
            self.construct_uml_occurrence_specification(covered_id=target_lifeline_id, interaction_id=interaction_id)

        send_event = self.get_instance_by_id(send_event_id)
        receive_event = self.get_instance_by_id(receive_event_id)

        signature = self.get_instance_by_id(signature_id)

        message = UmlMessage(
            id=id, name=name, send_event=send_event, receive_event=receive_event, sort=message_sort, kind=kind, signature=signature,
            model=self._model, builder=self
        )
        self.add_message(message)

        if send_event is None:
            self.register_dalayed_call_for_id(send_event_id, lambda event: setattr(message, 'send_event', event))

        if receive_event is None:
            self.register_dalayed_call_for_id(receive_event_id, lambda event: setattr(message, 'receive_event', event))        

        if interaction is None:
            def _queued_add_message_to_interaction(instance: UmlInteraction) -> None:
                instance.messages.append(message)
            
            self.register_dalayed_call_for_id(interaction_id, _queued_add_message_to_interaction)
        else:
            interaction.messages.append(message)

        if signature is None:
            self.register_dalayed_call_for_id(signature_id, lambda instance: setattr(message, 'signature', instance))

        return self

    def add_message(self, message: UmlMessage) -> "IUmlModelBuilder":
        self.add_element(message)
        return self

    # Interaction Elements
    def construct_uml_interaction(self, id: Optional[str] = None, name: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_interaction({args}, {kwargs})")
        interaction = UmlInteraction(id=id, name=name, model=self._model, builder=self)
        self.add_element(interaction)
        self.model.elements.interactions.append(interaction)
        return self

    def construct_uml_occurrence_specification(self, id: Optional[str] = None, covered_id: Optional[str] = None, interaction_id: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_occurrence_specification({args}, {kwargs})")
        
        covered_lifeline = self.get_instance_by_id(covered_id)
        interaction = self.get_instance_by_id(interaction_id)

        # TODO: call here self.construct_uml_occurrence_specification() for source and target lifelines
        occurence_event = UmlOccurrenceSpecification(id=id, covered=covered_lifeline, model=self._model, builder=self)
        self.add_element(occurence_event)

        if interaction is None:
            def _queued_add_occurrences_to_interaction(instance: UmlInteraction) -> None:
                instance.fragments.append(occurence_event)
            
            self.register_dalayed_call_for_id(interaction_id, _queued_add_occurrences_to_interaction)
        else:
            interaction.fragments.append(occurence_event)

        if covered_lifeline is None:
            self.register_dalayed_call_for_id(covered_id, lambda instance: setattr(occurence_event, 'covered', instance))

        return self

    def construct_uml_interaction_use(self, id: Optional[str] = None, covered_ids: Optional[List[str]] = None, referred_interaction_id: Optional[str] = None, parent_interaction_id: Optional[str] = None, name: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_interaction_use({args}, {kwargs})")
        covered = [self.get_instance_by_id(covered_id) for covered_id in (covered_ids or [])]
        referred_interaction = self.get_instance_by_id(referred_interaction_id)
        interaction_use = UmlInteractionUse(id=id, covered=covered, interaction=referred_interaction, model=self._model, builder=self)
        parent_interaction = self.get_instance_by_id(parent_interaction_id)

        self.add_element(interaction_use)

        if parent_interaction is not None:
            parent_interaction.fragments.append(interaction_use)
        else:
            def _queued_assign_interaction_use(interaction: UmlInteraction) -> None:
                interaction.fragments.append(interaction_use)
            
            self.register_dalayed_call_for_id(parent_interaction_id, _queued_assign_interaction_use)

        # Delayed assignments if covered elements or referred_interaction is not available
        for covered_id, covered_instance in zip(covered_ids or [], covered):
            if covered_instance is None:
                self.register_dalayed_call_for_id(covered_id, lambda instance: interaction_use.covered.append(instance))
        if referred_interaction is None:
            self.register_dalayed_call_for_id(referred_interaction_id, lambda instance: setattr(interaction_use, 'interaction', instance))

        return self

    def construct_uml_combined_fragment(self, id: Optional[str] = None, operand_ids: Optional[List[str]] = None, operator: Optional[str] = None, covered_ids: Optional[List[str]] = None, interaction_id: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_combined_fragment({args}, {kwargs})")
        operands = [self.get_instance_by_id(operand_id) for operand_id in (operand_ids or [])]
        covered = [self.get_instance_by_id(covered_id) for covered_id in (covered_ids or [])]
        interaction = self.get_instance_by_id(interaction_id)
        combined_fragment = UmlCombinedFragment(id=id, operands=operands, covered=covered, operator=operator, model=self._model, builder=self)
        self.add_element(combined_fragment)

        if interaction is not None:
            interaction.fragments.append(combined_fragment)
        else:
            def _queued_assign_combined_fragment(interaction: UmlInteraction) -> None:
                interaction.fragments.append(combined_fragment)
            
            self.register_dalayed_call_for_id(interaction_id, _queued_assign_combined_fragment)

        # Delayed assignments for operands and covered elements
        for operand_id, operand_instance in zip(operand_ids or [], operands):
            if operand_instance is None:
                self.register_dalayed_call_for_id(operand_id, lambda instance: combined_fragment.operands.append(instance))
        for covered_id, covered_instance in zip(covered_ids or [], covered):
            if covered_instance is None:
                self.register_dalayed_call_for_id(covered_id, lambda instance: combined_fragment.covered.append(instance))

        return self

    def construct_uml_operand(self, id: Optional[str] = None, guard: Optional[str] = None, fragment_ids: Optional[List[str]] = None, combined_fragment_id: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_operand({args}, {kwargs})")
        fragments = [self.get_instance_by_id(fragment_id) for fragment_id in (fragment_ids or [])]
        combined_fragment = self.get_instance_by_id(combined_fragment_id)

        operand = UmlOperand(id=id, guard=guard, fragments=fragments, model=self._model, builder=self)
        self.add_element(operand)
        
        if combined_fragment is not None:
            combined_fragment.operands.append(operand)
        else:
            def _queued_assign_operand(combined_fragment: UmlCombinedFragment) -> None:
                combined_fragment.operands.append(operand)
            
            self.register_dalayed_call_for_id(combined_fragment_id, _queued_assign_operand)

        # Delayed assignments for fragments
        for fragment_id, fragment_instance in zip(fragment_ids or [], fragments):
            if fragment_instance is None:
                self.register_dalayed_call_for_id(fragment_id, lambda instance: operand.fragments.append(instance))

        return self

    # Attributes and Operations
    def construct_uml_parameter(self, id: Optional[str] = None, name: Optional[str] = None, type_id: Optional[str] = None, operation_id: Optional[str] = None, direction: Optional[str] = UmlParameterDirectionEnum.IN, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_parameter({args}, {kwargs})")
        type = self.get_instance_by_id(type_id)
        parameter = UmlParameter(id=id, name=name, type=type, direction=direction, model=self._model, builder=self)
        operation = self.get_instance_by_id(operation_id)

        self.add_element(parameter)

        # Delayed assignment if type is not available
        if type is None:
            self.register_dalayed_call_for_id(type_id, lambda instance: setattr(parameter, 'type', instance))

        if operation is not None:
            operation.parameters.append(parameter)
        else:
            def _queued_assign_parameter(operation: UmlOperation) -> None:
                operation.parameters.append(parameter)
            
            self.register_dalayed_call_for_id(operation_id, _queued_assign_parameter)

        return self

    # Relationships
    def construct_uml_aggregation(self, id: Optional[str] = None, source_id: str = None, target_id: str = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_aggregation({args}, {kwargs})")
        source = self.get_instance_by_id(source_id)
        target = self.get_instance_by_id(target_id)
        
        aggregation = UmlAggregation(id=id, source=source, target=target, model=self._model, builder=self)
        self.add_element(aggregation)
        self.model.elements.associations.append(aggregation)

        # Delayed assignment if source or target is not available
        if source is None:
            self.register_dalayed_call_for_id(source_id, lambda instance: setattr(aggregation, 'source', instance))
        if target is None:
            self.register_dalayed_call_for_id(target_id, lambda instance: setattr(aggregation, 'target', instance))

        return self

    def construct_uml_composition(self, id: Optional[str] = None, source_id: str = None, target_id: str = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_composition({args}, {kwargs})")
        source = self.get_instance_by_id(source_id)
        target = self.get_instance_by_id(target_id)
        
        composition = UmlComposition(id=id, source=source, target=target, model=self._model, builder=self)
        self.add_element(composition)
        self.model.elements.associations.append(composition)

        # Delayed assignment if source or target is not available
        if source is None:
            self.register_dalayed_call_for_id(source_id, lambda instance: setattr(composition, 'source', instance))
        if target is None:
            self.register_dalayed_call_for_id(target_id, lambda instance: setattr(composition, 'target', instance))

        return self



    def _bind_not_initialized_element_to_diagram(self, element_id: str, diagram: Optional[UmlDiagram], diagram_id: Optional[str]) -> None:
        if diagram is not None:
            def _queued_assign_element_to_diagram(element: UmlElement) -> None:
                diagram.add_element(element)

            self.register_dalayed_call_for_id(element_id, _queued_assign_element_to_diagram)
        elif diagram_id is not None:
            def _queued_assign_element_to_diagram(element: UmlElement) -> None:
                self.bind_element_to_diagram(element=element, diagram_id=diagram_id)

            self.register_dalayed_call_for_id(element_id, _queued_assign_element_to_diagram)
        else:
            raise ValueError("Either diagram or diagram_id should be provided.")
         
    def _bind_initialized_element_to_diagram(self, element: UmlElement, diagram: Optional[UmlDiagram], diagram_id: Optional[str]) -> None:
        if diagram is not None:
            diagram.add_element(element)
        elif diagram_id is not None:
            def _queued_assign_element_to_diagram(diagram: UmlDiagram) -> None:
                diagram.add_element(element)
            
            self.register_dalayed_call_for_id(diagram_id, _queued_assign_element_to_diagram)
        else:
            raise ValueError("Either diagram or diagram_id should be provided.")

    def add_class_diagram(self, class_diagram: UmlClassDiagram) -> "IUmlModelBuilder":
        self.add_element(class_diagram)
        self.model.diagrams.class_diagrams.append(class_diagram)
        return self

    def add_sequence_diagram(self, sequence_diagram: UmlSequenceDiagram) -> "IUmlModelBuilder":
        self.add_element(sequence_diagram)
        self.model.diagrams.sequence_diagrams.append(sequence_diagram)
        return self

    def construct_sequence_diagram(self, id: Optional[str] = None, name: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_sequence_diagram({args}, {kwargs})")
        diagram = UmlSequenceDiagram(id=id, name=name, model=self._model, builder=self)
        self.add_sequence_diagram(diagram)
        return self

    def construct_class_diagram(self, id: Optional[str] = None, name: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_class_diagram({args}, {kwargs})")
        diagram = UmlClassDiagram(id=id, name=name, model=self._model, builder=self)
        self.add_class_diagram(diagram)
        return self

    def add_interaction(self, interaction: UmlInteraction) -> "IUmlModelBuilder":
        self.add_element(interaction)
        self.model.elements.interactions.append(interaction)
        return self

    # TODO: remove
    def __getattr__(self, name: str) -> "IUmlModelBuilder":
        def method(*args, **kwargs):
            self._logger.debug(f"Method called: {name}({args}, {kwargs})")
            return self
        return method
