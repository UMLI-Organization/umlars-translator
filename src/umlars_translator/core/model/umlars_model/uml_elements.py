from typing import List, Optional, Union, ClassVar, TYPE_CHECKING


from umlars_translator.core.model.umlars_model.mixins import RegisteredInModelMixin
from umlars_translator.core.model.abstract.uml_elements import IUmlElement, IUmlNamedElement, IUmlPrimitiveType, IUmlClassifier, IUmlClass, IUmlInterface, IUmlOrderedElement, IUmlDataType, IUmlEnumeration, IUmlAttribute, IUmlParameter, IUmlOperation, IUmlGeneralization, IUmlDependency, IUmlAssociationEnd, IUmlAssociationBase, IUmlAssociation, IUmlDirectedAssociation, IUmlAggregation, IUmlComposition, IUmlRealization, IUmlLifeline, IUmlMessage, IUmlCombinedFragment, IUmlInteractionUse, IUmlInteraction, IUmlPackage, IUmlOccurrenceSpecification, IUmlOperand, IUmlModelElements
from umlars_translator.core.model.constants import UmlVisibilityEnum, UmlMultiplicityEnum, UmlPrimitiveTypeKindEnum, UmlAssociationDirectionEnum, UmlParameterDirectionEnum, UmlInteractionOperatorEnum, UmlMessageSortEnum, UmlMessageKindEnum


# Base and Common Elements
class UmlElement(RegisteredInModelMixin, IUmlElement):
    ...


class UmlNamedElement(UmlElement, IUmlNamedElement):
    """
    Base class for all UML elements that have a name.
    """
    def __init__(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self._name = name
        self._visibility = visibility
        
    @property
    def name(self) -> Optional[str]:
        return self._name
    
    @name.setter
    def name(self, new_name: Optional[str]):
        self._name = new_name

    @property
    def visibility(self) -> UmlVisibilityEnum:
        return self._visibility
    
    @visibility.setter
    def visibility(self, new_visibility: UmlVisibilityEnum):
        self._visibility = new_visibility


# Primitive Types
class UmlPrimitiveType(IUmlPrimitiveType, UmlNamedElement):
    def __init__(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, kind: UmlPrimitiveTypeKindEnum = UmlPrimitiveTypeKindEnum.STRING, id: Optional[str] = None, **kwargs):
        super().__init__(name, visibility, id=id, **kwargs)
        self.kind = kind

    @property
    def kind(self) -> UmlPrimitiveTypeKindEnum:
        return self._kind

    @kind.setter
    def kind(self, new_kind: UmlPrimitiveTypeKindEnum):
        self._kind = new_kind


# Classifiers
class UmlClassifier(IUmlClassifier, UmlNamedElement):
    def __init__(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, attributes: Optional[List["UmlAttribute"]] = None, operations: Optional[List["UmlOperation"]] = None, id: Optional[str] = None, **kwargs):
        super().__init__(name, visibility, id=id, **kwargs)
        self.attributes = attributes or []
        self.operations = operations or []

    @property
    def attributes(self) -> List['UmlAttribute']:
        return self._attributes

    @attributes.setter
    def attributes(self, new_attributes: List['UmlAttribute']) -> None:
        self._attributes = new_attributes
        if self.builder:
            for attribute in new_attributes:
                self.builder.register_if_not_present(attribute)

    @property
    def operations(self) -> List['UmlOperation']:
        return self._operations

    @operations.setter
    def operations(self, new_operations: List['UmlOperation']):
        self._operations = new_operations
        if self.builder:
            for operation in new_operations:
                self.builder.register_if_not_present(operation)


class UmlClass(UmlClassifier, IUmlClass):
    def __init__(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, generalizations: Optional[List["UmlGeneralization"]] = None, interfaces: Optional[List["UmlInterface"]] = None, id: Optional[str] = None, **kwargs):
        super().__init__(name, visibility, id=id, **kwargs)
        self.generalizations = generalizations or []
        self.interfaces = interfaces or []

    @property
    def generalizations(self) -> List['UmlGeneralization']:
        return self._generalizations

    @generalizations.setter
    def generalizations(self, new_generalizations: List['UmlGeneralization']):
        self._generalizations = new_generalizations
        if self.builder:
            for generalization in new_generalizations:
                self.builder.register_if_not_present(generalization)

    @property
    def interfaces(self) -> List['UmlInterface']:
        return self._interfaces

    @interfaces.setter
    def interfaces(self, new_interfaces: List['UmlInterface']):
        self._interfaces = new_interfaces
        if self.builder:
            for interface in new_interfaces:
                self.builder.register_if_not_present(interface)


class UmlInterface(UmlClassifier, IUmlInterface):
    def __init__(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, id: Optional[str] = None, **kwargs):
        super().__init__(name, visibility, id=id, **kwargs)


class UmlDataType(UmlClassifier, IUmlDataType):
    def __init__(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, id: Optional[str] = None, **kwargs):
        super().__init__(name, visibility, id=id, **kwargs)


class UmlEnumeration(UmlNamedElement, IUmlEnumeration):
    def __init__(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, literals: Optional[List[str]] = None, id: Optional[str] = None, **kwargs):
        super().__init__(name, visibility, id=id, **kwargs)
        self.literals = literals or []

    @property
    def literals(self) -> List[str]:
        return self._literals

    @literals.setter
    def literals(self, new_literals: List[str]):
        self._literals = new_literals


# Attributes and Operations
class UmlAttribute(UmlNamedElement, IUmlAttribute):
    def __init__(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, type: Optional[Union[IUmlPrimitiveType, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration]] = None, is_static: Optional[bool] = None, is_ordered: Optional[bool] = None, is_unique: Optional[bool] = None, is_read_only: Optional[bool] = None, is_query: Optional[bool] = None, is_derived: Optional[bool] = None, is_derived_union: Optional[bool] = None, id: Optional[str] = None, **kwargs):
        super().__init__(name, visibility, id=id, **kwargs)
        self.type = type
        self.is_static = is_static
        self.is_ordered = is_ordered
        self.is_unique = is_unique
        self.is_read_only = is_read_only
        self.is_query = is_query
        self.is_derived = is_derived
        self.is_derived_union = is_derived_union

    @property
    def type(self) -> Union[IUmlPrimitiveType, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration]:
        return self._type
    
    @type.setter
    def type(self, new_type: Union[IUmlPrimitiveType, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration]):
        self._type = new_type
        if self.builder:
            self.builder.register_if_not_present(new_type)

    @property
    def is_static(self) -> Optional[bool]:
        return self._is_static
    
    @is_static.setter
    def is_static(self, new_is_static: Optional[bool]):
        self._is_static = new_is_static

    @property
    def is_ordered(self) -> Optional[bool]:
        return self._is_ordered
    
    @is_ordered.setter
    def is_ordered(self, new_is_ordered: Optional[bool]):
        self._is_ordered = new_is_ordered

    @property
    def is_unique(self) -> Optional[bool]:
        return self._is_unique
    
    @is_unique.setter
    def is_unique(self, new_is_unique: Optional[bool]):
        self._is_unique = new_is_unique

    @property
    def is_read_only(self) -> Optional[bool]:
        return self._is_read_only
    
    @is_read_only.setter
    def is_read_only(self, new_is_read_only: Optional[bool]):
        self._is_read_only = new_is_read_only

    @property
    def is_query(self) -> Optional[bool]:
        return self._is_query
    
    @is_query.setter
    def is_query(self, new_is_query: Optional[bool]):
        self._is_query = new_is_query

    @property
    def is_derived(self) -> Optional[bool]:
        return self._is_derived
    
    @is_derived.setter
    def is_derived(self, new_is_derived: Optional[bool]):
        self._is_derived = new_is_derived

    @property
    def is_derived_union(self) -> Optional[bool]:
        return self._is_derived_union
    
    @is_derived_union.setter
    def is_derived_union(self, new_is_derived_union: Optional[bool]):
        self._is_derived_union = new_is_derived_union

    
class UmlParameter(UmlNamedElement, IUmlParameter):
    def __init__(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, type: Optional[Union[IUmlPrimitiveType, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration]] = None, direction: UmlParameterDirectionEnum = UmlParameterDirectionEnum.IN, id: Optional[str] = None, **kwargs):
        super().__init__(name, visibility, id=id, **kwargs)
        self.type = type
        self.direction = direction

    @property
    def type(self) -> Union[IUmlPrimitiveType, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration]:
        return self._type
    
    @type.setter
    def type(self, new_type: Union[IUmlPrimitiveType, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration]):
        self._type = new_type
        if self.builder:
            self.builder.register_if_not_present(new_type)

    @property
    def direction(self) -> UmlParameterDirectionEnum:
        return self._direction
    
    @direction.setter
    def direction(self, new_direction: UmlParameterDirectionEnum):
        self._direction = new_direction


class UmlOperation(UmlNamedElement, IUmlOperation):
    def __init__(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, return_type: Optional[Union[IUmlPrimitiveType, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration]] = None, parameters: Optional[List[IUmlParameter]] = None, is_static: Optional[bool] = None, is_ordered: Optional[bool] = None, is_unique: Optional[bool] = None, is_query: Optional[bool] = None, is_derived: Optional[bool] = None, is_derived_union: Optional[bool] = None, is_abstract: bool = False, exceptions: Optional[List[str]] = None, id: Optional[str] = None, **kwargs):
        super().__init__(name, visibility, id=id, **kwargs)
        self.return_type = return_type
        self.parameters = parameters or []
        self.is_static = is_static
        self.is_ordered = is_ordered
        self.is_unique = is_unique
        self.is_query = is_query
        self.is_derived = is_derived
        self.is_derived_union = is_derived_union
        self.is_abstract = is_abstract
        self.exceptions = exceptions or []

    @property
    def return_type(self) -> Optional[Union[IUmlPrimitiveType, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration]]:
        return self._return_type
    
    @return_type.setter
    def return_type(self, new_return_type: Optional[Union[IUmlPrimitiveType, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration]]):
        self._return_type = new_return_type
        if self.builder:
            self.builder.register_if_not_present(new_return_type)

    @property
    def parameters(self) -> List[IUmlParameter]:
        return self._parameters
    
    @parameters.setter
    def parameters(self, new_parameters: List[IUmlParameter]):
        self._parameters = new_parameters
        if self.builder:
            for parameter in new_parameters:
                self.builder.register_if_not_present(parameter)

    @property
    def is_static(self) -> Optional[bool]:
        return self._is_static
    
    @is_static.setter
    def is_static(self, new_is_static: Optional[bool]):
        self._is_static = new_is_static

    @property
    def is_ordered(self) -> Optional[bool]:
        return self._is_ordered
    
    @is_ordered.setter
    def is_ordered(self, new_is_ordered: Optional[bool]):
        self._is_ordered = new_is_ordered

    @property
    def is_unique(self) -> Optional[bool]:
        return self._is_unique
    
    @is_unique.setter
    def is_unique(self, new_is_unique: Optional[bool]):
        self._is_unique = new_is_unique

    @property
    def is_query(self) -> Optional[bool]:
        return self._is_query
    
    @is_query.setter
    def is_query(self, new_is_query: Optional[bool]):
        self._is_query = new_is_query

    @property
    def is_derived(self) -> Optional[bool]:
        return self._is_derived
    
    @is_derived.setter
    def is_derived(self, new_is_derived: Optional[bool]):
        self._is_derived = new_is_derived

    @property
    def is_derived_union(self) -> Optional[bool]:
        return self._is_derived_union
    
    @is_derived_union.setter
    def is_derived_union(self, new_is_derived_union: Optional[bool]):
        self._is_derived_union = new_is_derived_union

    @property
    def is_abstract(self) -> bool:
        return self._is_abstract
    
    @is_abstract.setter
    def is_abstract(self, new_is_abstract: bool):
        self._is_abstract = new_is_abstract

    @property
    def exceptions(self) -> List[str]:
        return self._exceptions
    
    @exceptions.setter
    def exceptions(self, new_exceptions: List[str]):
        self._exceptions = new_exceptions

    
# Relationships
class UmlGeneralization(UmlElement, IUmlGeneralization):
    def __init__(self, specific: Optional[IUmlClass] = None, general: Optional[IUmlClass] = None, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.specific = specific
        self.general = general

    @property
    def specific(self) -> IUmlClass:
        return self._specific
    
    @specific.setter
    def specific(self, new_specific: IUmlClass):
        self._specific = new_specific
        if self.builder:
            self.builder.register_if_not_present(new_specific)

    @property
    def general(self) -> IUmlClass:
        return self._general
    
    @general.setter
    def general(self, new_general: IUmlClass):
        self._general = new_general
        if self.builder:
            self.builder.register_if_not_present(new_general)
    

class UmlDependency(UmlElement, IUmlDependency):
    def __init__(self, client: Optional[IUmlClassifier] = None, supplier: Optional[IUmlClassifier] = None, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.client = client
        self.supplier = supplier

    @property
    def client(self) -> IUmlElement:
        return self._client
    
    @client.setter
    def client(self, new_client: IUmlElement):
        self._client = new_client
        if self.builder:
            self.builder.register_if_not_present(new_client)

    @property
    def supplier(self) -> IUmlElement:
        return self._supplier
    
    @supplier.setter
    def supplier(self, new_supplier: IUmlElement):
        self._supplier = new_supplier
        if self.builder:
            self.builder.register_if_not_present(new_supplier)


class UmlRealization(UmlDependency, IUmlRealization):
    ...


# Associations
class UmlAssociationEnd(UmlNamedElement, IUmlAssociationEnd):
    def __init__(self, multiplicity: UmlMultiplicityEnum = UmlMultiplicityEnum.ONE, navigability: Optional[bool] = None, role: Optional[str] = None, element: Optional[IUmlClassifier] = None, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.multiplicity = multiplicity
        self.navigability = navigability
        self.role = role
        self.element = element

    @property
    def element(self) -> IUmlClassifier:
        return self._element
    
    @element.setter
    def element(self, new_element: IUmlClassifier):
        self._element = new_element
        if self.builder:
            self.builder.register_if_not_present(new_element)

    @property
    def role(self) -> Optional[str]:
        return self._role
    
    @role.setter
    def role(self, new_role: Optional[str]):
        self._role = new_role

    @property
    def multiplicity(self) -> UmlMultiplicityEnum:
        return self._multiplicity
    
    @multiplicity.setter
    def multiplicity(self, new_multiplicity: UmlMultiplicityEnum):
        self._multiplicity = new_multiplicity

    @property
    def navigability(self) -> bool:
        return self._navigability
    
    @navigability.setter
    def navigability(self, new_navigability: bool):
        self._navigability = new_navigability


class UmlAssociationBase(UmlNamedElement, IUmlAssociationBase):
    ASSOCIATION_DIRECTION: ClassVar[UmlAssociationDirectionEnum]

    def __init__(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, end1: Optional[IUmlAssociationEnd] = None, end2: Optional[IUmlAssociationEnd] = None, id: Optional[str] = None, **kwargs):
        super().__init__(name, visibility, id=id, **kwargs)
        self._end1 = end1
        self._end2 = end2

    @property
    def end1(self) -> IUmlAssociationEnd:
        return self._end1
    
    @property
    def end2(self) -> IUmlAssociationEnd:
        return self._end2
    
    @property
    def direction(self) -> UmlAssociationDirectionEnum:
        return self.association_direction()
    
    @classmethod
    def association_direction(cls) -> UmlAssociationDirectionEnum:
        return cls.ASSOCIATION_DIRECTION


class UmlAssociation(UmlAssociationBase, IUmlAssociation):
    ASSOCIATION_DIRECTION = UmlAssociationDirectionEnum.BIDIRECTIONAL

    def add_end(self, end: IUmlAssociationEnd):
        if not self.end1:
            self._end1 = end
        elif not self.end2:
            self._end2 = end
        else:
            raise ValueError("Both ends are already set")
        if self.builder:
            self.builder.register_if_not_present(end)

    def add_end1(self, end: IUmlAssociationEnd):
        self._end1 = end
        if self.builder:
            self.builder.register_if_not_present(end)

    def add_end2(self, end: IUmlAssociationEnd):
        self._end2 = end
        if self.builder:
            self.builder.register_if_not_present(end)


class UmlDirectedAssociation(UmlAssociationBase, IUmlDirectedAssociation):
    ASSOCIATION_DIRECTION = UmlAssociationDirectionEnum.DIRECTED

    def __init__(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, source: Optional[IUmlAssociationEnd]=None, target: Optional[IUmlAssociationEnd]=None, id: Optional[str] = None, **kwargs):
        super().__init__(name=name, visibility=visibility, id=id, **kwargs)
        self._source = source
        self._target = target

    @property
    def source(self) -> IUmlAssociationEnd:
        return self._source
    
    @property
    def target(self) -> IUmlAssociationEnd:
        return self._target

    @source.setter
    def source(self, new_source: IUmlAssociationEnd):
        self._source = new_source
        self._end1 = new_source
        if self.builder:
            self.builder.register_if_not_present(new_source)

    @target.setter
    def target(self, new_target: IUmlAssociationEnd):
        self._target = new_target
        self._end2 = new_target
        if self.builder:
            self.builder.register_if_not_present(new_target)

    @property
    def end1(self) -> IUmlAssociationEnd:
        return self.source
    
    @property
    def end2(self) -> IUmlAssociationEnd:
        return self.target


class UmlAggregation(UmlDirectedAssociation, IUmlAggregation):
    ...


class UmlComposition(UmlDirectedAssociation, IUmlComposition):
    ...


# Interaction
class UmlOrderedElement(IUmlOrderedElement):
    def __init__(self, ordering_key: int, **kwargs):
        self._ordering_key = ordering_key

    @property
    def ordering_key(self) -> int:
        return self._ordering_key

    @ordering_key.setter
    def ordering_key(self, new_ordering_key: int):
        self._ordering_key = new_ordering_key


class UmlOccurrenceSpecification(UmlElement, UmlOrderedElement, IUmlOccurrenceSpecification):
    def __init__(self, covered: IUmlLifeline, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.covered = covered

    @property
    def covered(self) -> IUmlLifeline:
        return self._covered
    
    @covered.setter
    def covered(self, new_covered: IUmlLifeline):
        self._covered = new_covered
        if self.builder:
            self.builder.register_if_not_present(new_covered)

    
class UmlCombinedFragment(UmlNamedElement, UmlOrderedElement, IUmlCombinedFragment):
    def __init__(self, operator: UmlInteractionOperatorEnum, operands: List[IUmlOperand], covered: List["UmlLifeline"], id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.operator = operator
        self.operands = operands or []
        self.covered = covered

    @property
    def operator(self) -> UmlInteractionOperatorEnum:
        return self._operator
    
    @operator.setter
    def operator(self, new_operator: UmlInteractionOperatorEnum):
        self._operator = new_operator

    @property
    def operands(self) -> List[IUmlOperand]:
        return self._operands
    
    @operands.setter
    def operands(self, new_operands: List[IUmlOperand]):
        self._operands = new_operands
        if self.builder:
            for operand in new_operands:
                self.builder.register_if_not_present(operand)

    @property
    def covered(self) -> List["UmlLifeline"]:
        return self._covered
    
    @covered.setter
    def covered(self, new_covered: List["UmlLifeline"]):
        self._covered = new_covered
        if self.builder:
            for lifeline in new_covered:
                self.builder.register_if_not_present(lifeline)

    
class UmlInteractionUse(UmlNamedElement, UmlOrderedElement, IUmlInteractionUse):
    def __init__(self, covered: List["UmlLifeline"], interaction: "UmlInteraction", id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.covered = covered
        self.interaction = interaction

    @property
    def covered(self) -> List["UmlLifeline"]:
        return self._covered
    
    @covered.setter
    def covered(self, new_covered: List["UmlLifeline"]):
        self._covered = new_covered
        if self.builder:
            for lifeline in new_covered:
                self.builder.register_if_not_present(lifeline)

    @property
    def interaction(self) -> "UmlInteraction":
        return self._interaction
    
    @interaction.setter
    def interaction(self, new_interaction: "UmlInteraction"):
        self._interaction = new_interaction
        if self.builder:
            self.builder.register_if_not_present(new_interaction)


class UmlOperand(UmlElement, IUmlOperand):
    def __init__(self, guard: Optional[str], fragments: List[Union[IUmlOccurrenceSpecification, IUmlInteractionUse, IUmlCombinedFragment]], id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.guard = guard
        self.fragments = fragments

    @property
    def guard(self) -> Optional[str]:
        return self._guard
    
    @guard.setter
    def guard(self, new_guard: Optional[str]):
        self._guard = new_guard

    @property
    def fragments(self) -> List[Union[IUmlOccurrenceSpecification, IUmlInteractionUse, IUmlCombinedFragment]]:
        return self._fragments
    
    # TODO: such setters do not cope with case, when someone just uses 'append' method on the list
    # In such scenario the new object may not be added to the builder
    @fragments.setter
    def fragments(self, new_fragments: List[Union[IUmlOccurrenceSpecification, IUmlInteractionUse, IUmlCombinedFragment]]):
        self._fragments = new_fragments
        if self.builder:
            for fragment in new_fragments:
                self.builder.register_if_not_present(fragment)


class UmlMessage(UmlNamedElement, IUmlMessage):
    def __init__(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, sort: UmlMessageSortEnum = UmlMessageSortEnum.SYNCH_CALL, kind: UmlMessageKindEnum = UmlMessageKindEnum.UNKNOWN, send_event: Optional[IUmlOccurrenceSpecification] = None, receive_event: Optional[IUmlOccurrenceSpecification] = None, signature: Optional[IUmlOperation] = None, arguments: Optional[List[str]] = None, id: Optional[str] = None, **kwargs):
        super().__init__(name, visibility, id=id, **kwargs)
        self.sort = sort
        self.kind = kind
        self.send_event = send_event
        self.receive_event = receive_event
        self.signature = signature
        self.arguments = arguments or []

    @property
    def send_event(self) -> IUmlOccurrenceSpecification:
        return self._send_event
    
    @send_event.setter
    def send_event(self, new_send_event: IUmlOccurrenceSpecification):
        self._send_event = new_send_event
        if self.builder:
            self.builder.register_if_not_present(new_send_event)

    @property
    def receive_event(self) -> IUmlOccurrenceSpecification:
        return self._receive_event
    
    @receive_event.setter
    def receive_event(self, new_receive_event: IUmlOccurrenceSpecification):
        self._receive_event = new_receive_event
        if self.builder:
            self.builder.register_if_not_present(new_receive_event)

    @property
    def signature(self) -> Optional[IUmlOperation]:
        return self._signature
    
    @signature.setter
    def signature(self, new_signature: Optional[IUmlOperation]):
        self._signature = new_signature
        if self.builder:
            self.builder.register_if_not_present(new_signature)

    @property
    def arguments(self) -> List[str]:
        return self._arguments
    
    @arguments.setter
    def arguments(self, new_arguments: List[str]):
        self._arguments = new_arguments

    @property
    def sort(self) -> UmlMessageSortEnum:
        return self._sort
    
    @sort.setter
    def sort(self, new_sort: UmlMessageSortEnum):
        self._sort = new_sort

    @property
    def kind(self) -> UmlMessageKindEnum:
        return self._kind
    
    @kind.setter
    def kind(self, new_kind: UmlMessageKindEnum):
        self._kind = new_kind


class UmlLifeline(UmlNamedElement, IUmlLifeline):
    def __init__(self, name: Optional[str] = None, visibility: Optional[UmlVisibilityEnum] = UmlVisibilityEnum.PUBLIC, represents: Optional[UmlClassifier] = None, id: Optional[str] = None, **kwargs):
        super().__init__(name, visibility, id=id, **kwargs)
        self.represents = represents

    @property
    def represents(self) -> UmlClassifier:
        return self._represents
    
    @represents.setter
    def represents(self, new_represents: UmlClassifier):
        self._represents = new_represents
        if self.builder:
            self.builder.register_if_not_present(new_represents)


class UmlInteraction(UmlNamedElement, IUmlInteraction):
    def __init__(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, lifelines: Optional[List[IUmlLifeline]] = None, messages: Optional[List[IUmlMessage]] = None, fragments: Optional[List[Union[IUmlOccurrenceSpecification, IUmlInteractionUse, IUmlCombinedFragment]]] = None, user_ordering_keys: bool = False, id: Optional[str] = None, **kwargs):
        super().__init__(name, visibility, id=id, **kwargs)
        self.lifelines = lifelines or []
        self.messages = messages or []
        self.fragments = fragments or []
        self._user_ordering_keys = user_ordering_keys

    @property
    def fragments(self) -> List[Union[IUmlOccurrenceSpecification, IUmlInteractionUse, IUmlCombinedFragment]]:
        if self.user_ordering_keys:
            return sorted(self._fragments, key=lambda x: x.ordering_key)
        return self._fragments
    
    @fragments.setter
    def fragments(self, new_fragments: List[Union[IUmlOccurrenceSpecification, IUmlInteractionUse, IUmlCombinedFragment]]):
        self._fragments = new_fragments
        if self.builder:
            for i, fragment in enumerate(new_fragments):
                self.builder.register_if_not_present(fragment)
                fragment.ordering_key = i
        else:
            for i, fragment in enumerate(new_fragments):
                fragment.ordering_key = i
        
    def set_fragments(self, new_fragments: List[Union[IUmlOccurrenceSpecification, IUmlInteractionUse, IUmlCombinedFragment]], sort_by_ordering_key: bool = False):
        if sort_by_ordering_key:
            new_fragments = sorted(new_fragments, key=lambda x: x.ordering_key) if sort_by_ordering_key else new_fragments
    
        self.fragments = new_fragments

    @property
    def lifelines(self) -> List[IUmlLifeline]:
        return self._lifelines
    
    @lifelines.setter
    def lifelines(self, new_lifelines: List[IUmlLifeline]):
        self._lifelines = new_lifelines
        if self.builder:
            for lifeline in new_lifelines:
                self.builder.register_if_not_present(lifeline)

    @property
    def messages(self) -> List[IUmlMessage]:
        return self._messages
    
    @messages.setter
    def messages(self, new_messages: List[IUmlMessage]):
        self._messages = new_messages
        if self.builder:
            for message in new_messages:
                self.builder.register_if_not_present(message)

    @property
    def user_ordering_keys(self) -> bool:
        return self._user_ordering_keys
    
    @user_ordering_keys.setter
    def user_ordering_keys(self, new_user_ordering_keys: bool):
        self._user_ordering_keys = new_user_ordering_keys


class UmlModelElements(UmlElement, IUmlModelElements):
    def __init__(self, classes: Optional[List[IUmlClass]] = None, interfaces: Optional[List[IUmlInterface]] = None, data_types: Optional[List[IUmlDataType]] = None, enumerations: Optional[List[IUmlEnumeration]] = None, primitive_types: Optional[List[IUmlPrimitiveType]] = None, associations: Optional[List[Union[IUmlAssociation, IUmlDirectedAssociation]]] = None, generalizations: Optional[List[IUmlGeneralization]] = None, dependencies: Optional[List[IUmlDependency]] = None, realizations: Optional[List[IUmlRealization]] = None, interactions: Optional[List[IUmlInteraction]] = None, packages: Optional[List[IUmlPackage]] = None, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.classes = classes or []
        self.interfaces = interfaces or []
        self.data_types = data_types or []
        self.enumerations = enumerations or []
        self.primitive_types = primitive_types or []
        self.associations = associations or []
        self.generalizations = generalizations or []
        self.dependencies = dependencies or []
        self.realizations = realizations or []
        self.interactions = interactions or []
        self.packages = packages or []

    @property
    def classes(self) -> List[IUmlClass]:
        return self._classes
    
    @classes.setter
    def classes(self, new_classes: Optional[List[IUmlClass]]):
        self._classes = new_classes or []
        if self.builder:
            for uml_class in self._classes:
                self.builder.register_if_not_present(uml_class)

    @property
    def interfaces(self) -> List[IUmlInterface]:
        return self._interfaces
    
    @interfaces.setter
    def interfaces(self, new_interfaces: Optional[List[IUmlInterface]]):
        self._interfaces = new_interfaces or []
        if self.builder:
            for interface in self._interfaces:
                self.builder.register_if_not_present(interface)

    @property
    def data_types(self) -> List[IUmlDataType]:
        return self._data_types
    
    @data_types.setter
    def data_types(self, new_data_types: Optional[List[IUmlDataType]]):
        self._data_types = new_data_types or []
        if self.builder:
            for data_type in self._data_types:
                self.builder.register_if_not_present(data_type)

    @property
    def enumerations(self) -> List[IUmlEnumeration]:
        return self._enumerations
    
    @enumerations.setter
    def enumerations(self, new_enumerations: Optional[List[IUmlEnumeration]]):
        self._enumerations = new_enumerations or []
        if self.builder:
            for enumeration in self._enumerations:
                self.builder.register_if_not_present(enumeration)

    @property
    def primitive_types(self) -> List[IUmlPrimitiveType]:
        return self._primitive_types
    
    @primitive_types.setter
    def primitive_types(self, new_primitive_types: Optional[List[IUmlPrimitiveType]]):
        self._primitive_types = new_primitive_types or []
        if self.builder:
            for primitive_type in self._primitive_types:
                self.builder.register_if_not_present(primitive_type)

    @property
    def associations(self) -> List[Union[IUmlAssociation, IUmlDirectedAssociation]]:
        return self._associations
    
    @associations.setter
    def associations(self, new_associations: Optional[List[Union[IUmlAssociation, IUmlDirectedAssociation]]]):
        self._associations = new_associations or []
        if self.builder:
            for association in self._associations:
                self.builder.register_if_not_present(association)

    @property
    def generalizations(self) -> List[IUmlGeneralization]:
        return self._generalizations
    
    @generalizations.setter
    def generalizations(self, new_generalizations: Optional[List[IUmlGeneralization]]):
        self._generalizations = new_generalizations or []
        if self.builder:
            for generalization in self._generalizations:
                self.builder.register_if_not_present(generalization)

    @property
    def dependencies(self) -> List[IUmlDependency]:
        return self._dependencies
    
    @dependencies.setter
    def dependencies(self, new_dependencies: Optional[List[IUmlDependency]]):
        self._dependencies = new_dependencies or []
        if self.builder:
            for dependency in self._dependencies:
                self.builder.register_if_not_present(dependency)

    @property
    def realizations(self) -> List[IUmlRealization]:
        return self._realizations
    
    @realizations.setter
    def realizations(self, new_realizations: Optional[List[IUmlRealization]]):
        self._realizations = new_realizations or []
        if self.builder:
            for realization in self._realizations:
                self.builder.register_if_not_present(realization)

    @property
    def interactions(self) -> List[IUmlInteraction]:
        return self._interactions
    
    @interactions.setter
    def interactions(self, new_interactions: Optional[List[IUmlInteraction]]):
        self._interactions = new_interactions or []
        if self.builder:
            for interaction in self._interactions:
                self.builder.register_if_not_present(interaction)

    @property
    def packages(self) -> List[IUmlPackage]:
        return self._packages
    
    @packages.setter
    def packages(self, new_packages: Optional[List[IUmlPackage]]):
        self._packages = new_packages or []
        if self.builder:
            for package in self._packages:
                self.builder.register_if_not_present(package)


class UmlPackage(UmlNamedElement, IUmlPackage):
    def __init__(self, name: Optional[str] = None, visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC, elements: Optional[IUmlModelElements] = None, id: Optional[str] = None, **kwargs):
        super().__init__(name, visibility, id=id, **kwargs)
        self.elements = elements or UmlModelElements()

    @property
    def elements(self) -> IUmlModelElements:
        return self._elements
    
    @elements.setter
    def elements(self, new_elements: IUmlModelElements):
        self._elements = new_elements
        if self.builder:
            self.builder.register_if_not_present(new_elements)

    def add_class(self, uml_class: IUmlClass):
        self.elements.classes.append(uml_class)
        if self.builder:
            self.builder.register_if_not_present(uml_class)

    def add_interface(self, uml_interface: IUmlInterface):
        self.elements.interfaces.append(uml_interface)
        if self.builder:
            self.builder.register_if_not_present(uml_interface)

    def add_association(self, association: Union[IUmlAssociation, IUmlDirectedAssociation]):
        self.elements.associations.append(association)
        if self.builder:
            self.builder.register_if_not_present(association)

    def add_generalization(self, generalization: IUmlGeneralization):
        self.elements.generalizations.append(generalization)
        if self.builder:
            self.builder.register_if_not_present(generalization)

    def add_dependency(self, dependency: IUmlDependency):
        self.elements.dependencies.append(dependency)
        if self.builder:
            self.builder.register_if_not_present(dependency)

    def add_realization(self, realization: IUmlRealization):
        self.elements.realizations.append(realization)
        if self.builder:
            self.builder.register_if_not_present(realization)

    def add_interaction(self, interaction: IUmlInteraction):
        self.elements.interactions.append(interaction)
        if self.builder:
            self.builder.register_if_not_present(interaction)

    def add_package(self, package: IUmlPackage):
        self.elements.packages.append(package)
        if self.builder:
            self.builder.register_if_not_present(package)

    def add_data_type(self, data_type: IUmlDataType):
        self.elements.data_types.append(data_type)
        if self.builder:
            self.builder.register_if_not_present(data_type)

    def add_enumeration(self, enumeration: IUmlEnumeration):
        self.elements.enumerations.append(enumeration)
        if self.builder:
            self.builder.register_if_not_present(enumeration)

    def add_primitive_type(self, primitive_type: IUmlPrimitiveType):
        self.elements.primitive_types.append(primitive_type)
        if self.builder:
            self.builder.register_if_not_present(primitive_type)
