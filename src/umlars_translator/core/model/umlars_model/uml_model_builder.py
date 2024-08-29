from typing import Any, Optional, List, Union
from logging import Logger

from kink import inject

from src.umlars_translator.core.model.abstract.uml_model_builder import IUmlModelBuilder
from src.umlars_translator.core.model.umlars_model.uml_model import UmlModel
from src.umlars_translator.core.model.umlars_model.uml_elements import (
    UmlElement, UmlClass, UmlLifeline, UmlAssociationEnd, UmlAssociationBase, UmlVisibilityEnum, UmlInterface,
    UmlPackage, UmlPrimitiveType, UmlAttribute, UmlOperation, UmlLifeline, UmlAssociationEnd, UmlAssociationBase,
    UmlAggregation, UmlComposition, UmlRealization, UmlGeneralization, UmlDependency, UmlDirectedAssociation,
    UmlAssociation, UmlDataType, UmlEnumeration, UmlParameter, UmlMessage, UmlInteraction, UmlOccurrenceSpecification,
    UmlInteractionUse, UmlCombinedFragment, UmlOperand
)
from src.umlars_translator.core.utils.delayed_caller import (
    DalayedIdToInstanceMapper,
    evaluate_elements_afterwards,
)
from src.umlars_translator.core.model.umlars_model.uml_diagrams import UmlDiagram
from src.umlars_translator.core.model.constants import UmlVisibilityEnum, UmlMultiplicityEnum, UmlPrimitiveTypeKindEnum, UmlParameterDirectionEnum, UmlInteractionOperatorEnum, UmlMessageSortEnum, UmlMessageKindEnum


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

    def construct_uml_attribute(self, id: Optional[str] = None, name: Optional[str] = None, visibility: Optional[UmlVisibilityEnum] = UmlVisibilityEnum.PUBLIC, type_id: Optional[str] = None, is_static: Optional[bool] = None, is_ordered: Optional[bool] = None, is_unique: Optional[bool] = None, is_read_only: Optional[bool] = None, is_query: Optional[bool] = None, is_derived: Optional[bool] = None, is_derived_union: Optional[bool] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_attribute({args}, {kwargs})")
        type = self.get_instance_by_id(type_id)
        attribute = UmlAttribute(id=id, name=name, type=type, visibility=visibility, is_static=is_static, is_ordered=is_ordered, is_unique=is_unique, is_read_only=is_read_only, is_query=is_query, is_derived=is_derived, is_derived_union=is_derived_union, model=self._model, builder=self)
        self.add_attribute(attribute)

        if type is None:
            def _queued_assign_type(type: UmlElement) -> None:
                attribute.type = type
            
            self.register_dalayed_call_for_id(type_id, _queued_assign_type)

        return self

    def add_attribute(self, attribute: UmlAttribute) -> "IUmlModelBuilder":
        self.add_element(attribute)
        return self

    def construct_uml_operation(self, id: Optional[str] = None, name: Optional[str] = None, visibility: Optional[UmlVisibilityEnum] = UmlVisibilityEnum.PUBLIC, return_type_id: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_operation({args}, {kwargs})")
        return_type = self.get_instance_by_id(return_type_id)
        operation = UmlOperation(id=id, name=name, return_type=return_type, visibility=visibility, model=self._model, builder=self)
        self.add_operation(operation)

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

    def construct_uml_lifeline(self, id: Optional[str] = None, name: Optional[str] = None, represents_id: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_lifeline({args}, {kwargs})")
        represents = self.get_instance_by_id(represents_id)
        lifeline = UmlLifeline(id=id, name=name, represents=represents, model=self._model, builder=self)
        self.add_lifeline(lifeline)

        if represents is None:
            def _queued_assign_represents(element: UmlElement) -> None:
                lifeline.represents = element
            
            self.register_dalayed_call_for_id(represents_id, _queued_assign_represents)

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
        element_id: Optional[str] = None, 
        role: Optional[str] = None, 
        multiplicity: Optional[UmlMultiplicityEnum] = UmlMultiplicityEnum.ONE, 
        navigability: bool = True, 
        association_id: Optional[str] = None,
        *args, 
        **kwargs
    ) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_association_end({args}, {kwargs})")
        element = self.get_instance_by_id(element_id)
        association = self.get_instance_by_id(association_id)

        association_end = UmlAssociationEnd(
            id=id, 
            element=element, 
            role=role, 
            multiplicity=multiplicity, 
            navigability=navigability, 
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
            self.register_dalayed_call_for_id(element_id, lambda instance: _queued_assign_element(instance))

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

    def construct_uml_message(self, id: Optional[str] = None, name: Optional[str] = None, send_event_id: Optional[str] = None, receive_event_id: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_message({args}, {kwargs})")
        send_event = self.get_instance_by_id(send_event_id)
        receive_event = self.get_instance_by_id(receive_event_id)
        message = UmlMessage(id=id, name=name, send_event=send_event, receive_event=receive_event, model=self._model, builder=self)
        self.add_message(message)

        if send_event is None:
            self.register_dalayed_call_for_id(send_event_id, lambda e: setattr(message, 'send_event', e))
        if receive_event is None:
            self.register_dalayed_call_for_id(receive_event_id, lambda e: setattr(message, 'receive_event', e))

        return self

    def add_message(self, message: UmlMessage) -> "IUmlModelBuilder":
        self.add_element(message)
        self.model.elements.messages.append(message)
        return self

    # Interaction Elements
    def construct_uml_interaction(self, id: Optional[str] = None, name: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_interaction({args}, {kwargs})")
        interaction = UmlInteraction(id=id, name=name, model=self._model, builder=self)
        self.add_element(interaction)
        self.model.elements.interactions.append(interaction)
        return self

    def construct_uml_occurrence_specification(self, id: Optional[str] = None, covered_id: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_occurrence_specification({args}, {kwargs})")
        covered = self.get_instance_by_id(covered_id)
        occurrence = UmlOccurrenceSpecification(id=id, covered=covered, model=self._model, builder=self)
        self.add_element(occurrence)
        self.model.elements.occurrence_specifications.append(occurrence)

        # Delayed assignment if covered is not available
        if covered is None:
            self.register_dalayed_call_for_id(covered_id, lambda instance: setattr(occurrence, 'covered', instance))

        return self

    def construct_uml_interaction_use(self, id: Optional[str] = None, covered_ids: Optional[List[str]] = None, interaction_id: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_interaction_use({args}, {kwargs})")
        covered = [self.get_instance_by_id(covered_id) for covered_id in (covered_ids or [])]
        interaction = self.get_instance_by_id(interaction_id)
        interaction_use = UmlInteractionUse(id=id, covered=covered, interaction=interaction, model=self._model, builder=self)
        self.add_element(interaction_use)
        self.model.elements.interaction_uses.append(interaction_use)

        # Delayed assignments if covered elements or interaction is not available
        for covered_id, covered_instance in zip(covered_ids or [], covered):
            if covered_instance is None:
                self.register_dalayed_call_for_id(covered_id, lambda instance: interaction_use.covered.append(instance))
        if interaction is None:
            self.register_dalayed_call_for_id(interaction_id, lambda instance: setattr(interaction_use, 'interaction', instance))

        return self

    def construct_uml_combined_fragment(self, id: Optional[str] = None, operand_ids: Optional[List[str]] = None, operator: Optional[str] = None, covered_ids: Optional[List[str]] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_combined_fragment({args}, {kwargs})")
        operands = [self.get_instance_by_id(operand_id) for operand_id in (operand_ids or [])]
        covered = [self.get_instance_by_id(covered_id) for covered_id in (covered_ids or [])]
        combined_fragment = UmlCombinedFragment(id=id, operands=operands, covered=covered, operator=operator, model=self._model, builder=self)
        self.add_element(combined_fragment)
        self.model.elements.combined_fragments.append(combined_fragment)

        # Delayed assignments for operands and covered elements
        for operand_id, operand_instance in zip(operand_ids or [], operands):
            if operand_instance is None:
                self.register_dalayed_call_for_id(operand_id, lambda instance: combined_fragment.operands.append(instance))
        for covered_id, covered_instance in zip(covered_ids or [], covered):
            if covered_instance is None:
                self.register_dalayed_call_for_id(covered_id, lambda instance: combined_fragment.covered.append(instance))

        return self

    def construct_uml_operand(self, id: Optional[str] = None, guard: Optional[str] = None, fragment_ids: Optional[List[str]] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_operand({args}, {kwargs})")
        fragments = [self.get_instance_by_id(fragment_id) for fragment_id in (fragment_ids or [])]
        operand = UmlOperand(id=id, guard=guard, fragments=fragments, model=self._model, builder=self)
        self.add_element(operand)
        self.model.elements.operands.append(operand)

        # Delayed assignments for fragments
        for fragment_id, fragment_instance in zip(fragment_ids or [], fragments):
            if fragment_instance is None:
                self.register_dalayed_call_for_id(fragment_id, lambda instance: operand.fragments.append(instance))

        return self

    # Attributes and Operations
    def construct_uml_parameter(self, id: Optional[str] = None, name: Optional[str] = None, type_id: Optional[str] = None, direction: Optional[str] = None, *args, **kwargs) -> "IUmlModelBuilder":
        self._logger.debug(f"Method called: construct_uml_parameter({args}, {kwargs})")
        type = self.get_instance_by_id(type_id)
        parameter = UmlParameter(id=id, name=name, type=type, direction=direction, model=self._model, builder=self)
        self.add_element(parameter)
        self.model.elements.parameters.append(parameter)

        # Delayed assignment if type is not available
        if type is None:
            self.register_dalayed_call_for_id(type_id, lambda instance: setattr(parameter, 'type', instance))

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

    def __getattr__(self, name: str) -> "IUmlModelBuilder":
        def method(*args, **kwargs):
            self._logger.debug(f"Method called: {name}({args}, {kwargs})")
            return self

        return method
