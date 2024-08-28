from dataclasses import dataclass, field
from typing import List, Optional, Union, ClassVar

from dataclass_wizard import property_wizard

from src.umlars_translator.core.model.umlars_model.mixins import RegisteredInModelMixin, NamedElementMixin
from src.umlars_translator.core.model.abstract.uml_elements import IUmlElement, IUmlNamedElement, IUmlPrimitiveType, IUmlClassifier, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration, IUmlAttribute, IUmlParameter, IUmlOperation, IUmlGeneralization, IUmlDependency, IUmlAssociationEnd, IUmlAssociationBase, IUmlAssociation, IUmlDirectedAssociation, IUmlAggregation, IUmlComposition, IUmlRealization, IUmlLifeline, IUmlMessage, IUmlFragment, IUmlInteractionOperand, IUmlInteraction, IUmlPackage
from src.umlars_translator.core.model.constants import UmlVisibilityEnum, UmlMultiplicityEnum, UmlPrimitiveTypeKindEnum, UmlAssociationDirectionEnum


@dataclass
class UmlElement(RegisteredInModelMixin, IUmlElement, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]]

    @classmethod
    def element_name(cls) -> str:
        try:
            return cls.__ELEMENT_NAME
        except AttributeError:
            return cls.__name__


@dataclass(kw_only=True)
class UmlNamedElement(UmlElement, NamedElementMixin, IUmlNamedElement, metaclass=property_wizard):
    """
    Base class for all UML elements that have a name.
    """


@dataclass(kw_only=True)
class UmlPrimitiveType(IUmlPrimitiveType, UmlNamedElement, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlPrimitiveType'
    kind: UmlPrimitiveTypeKindEnum

    @property
    def kind(self) -> UmlPrimitiveTypeKindEnum:
        return self._kind

    @kind.setter
    def kind(self, new_kind: UmlPrimitiveTypeKindEnum):
        self._kind = new_kind


# Classifiers
@dataclass(kw_only=True)
class UmlClassifier(IUmlClassifier, UmlNamedElement, metaclass=property_wizard):
    visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC
    attributes: List['UmlAttribute'] = field(default_factory=list)
    operations: List['UmlOperation'] = field(default_factory=list)

    @property
    def attributes(self) -> List['UmlAttribute']:
        return self._attributes

    @attributes.setter
    def attributes(self, new_attributes: List['UmlAttribute']):
        self._attributes = new_attributes
        if self.builder:
            for attr in new_attributes:
                self.builder.register_if_not_present(attr)

    @property
    def operations(self) -> List['UmlOperation']:
        return self._operations

    @operations.setter
    def operations(self, new_operations: List['UmlOperation']):
        self._operations = new_operations
        if self.builder:
            for op in new_operations:
                self.builder.register_if_not_present(op)


@dataclass(kw_only=True)
class UmlClass(IUmlClass, UmlClassifier, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlClass'
    super_classes: List['UmlGeneralization'] = field(default_factory=list)
    interfaces: List['UmlInterface'] = field(default_factory=list)

    @property
    def super_classes(self) -> List['UmlGeneralization']:
        return self._super_classes

    @super_classes.setter
    def super_classes(self, new_super_classes: List['UmlGeneralization']):
        self._super_classes = new_super_classes
        if self.builder:
            for super_class in new_super_classes:
                self.builder.register_if_not_present(super_class)

    @property
    def interfaces(self) -> List['UmlInterface']:
        return self._interfaces

    @interfaces.setter
    def interfaces(self, new_interfaces: List['UmlInterface']):
        self._interfaces = new_interfaces
        if self.builder:
            for interface in new_interfaces:
                self.builder.register_if_not_present(interface)


@dataclass(kw_only=True)
class UmlInterface(IUmlInterface, UmlClassifier, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlInterface'


@dataclass(kw_only=True)
class UmlDataType(IUmlDataType, UmlClassifier, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlDataType'


@dataclass(kw_only=True)
class UmlEnumeration(IUmlEnumeration, UmlNamedElement, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlEnumeration'
    literals: List[str] = field(default_factory=list)

    @property
    def literals(self) -> List[str]:
        return self._literals

    @literals.setter
    def literals(self, new_literals: List[str]):
        self._literals = new_literals


# Attributes and Operations
@dataclass(kw_only=True)
class UmlAttribute(IUmlAttribute, UmlNamedElement, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlAttribute'
    type: Union[UmlPrimitiveType, UmlClass, UmlInterface, UmlDataType, UmlEnumeration]
    visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC
    is_static: Optional[bool] = None
    is_ordered: Optional[bool] = None
    is_unique: Optional[bool] = None
    is_read_only: Optional[bool] = None
    is_query: Optional[bool] = None
    is_derived: Optional[bool] = None
    is_derived_union: Optional[bool] = None

    @property
    def type(self) -> Union[UmlPrimitiveType, UmlClass, UmlInterface, UmlDataType, UmlEnumeration]:
        return self._type

    @type.setter
    def type(self, new_type: Union[UmlPrimitiveType, UmlClass, UmlInterface, UmlDataType, UmlEnumeration]):
        self._type = new_type
        if self.builder:
            self.builder.register_if_not_present(new_type)


@dataclass(kw_only=True)
class UmlParameter(IUmlParameter, UmlNamedElement, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlParameter'
    type: Union[UmlPrimitiveType, UmlClass, UmlInterface, UmlDataType, UmlEnumeration]

    @property
    def type(self) -> Union[UmlPrimitiveType, UmlClass, UmlInterface, UmlDataType, UmlEnumeration]:
        return self._type

    @type.setter
    def type(self, new_type: Union[UmlPrimitiveType, UmlClass, UmlInterface, UmlDataType, UmlEnumeration]):
        self._type = new_type
        if self.builder:
            self.builder.register_if_not_present(new_type)


@dataclass(kw_only=True)
class UmlOperation(IUmlOperation, UmlNamedElement, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlOperation'
    return_type: Optional[Union[UmlPrimitiveType, UmlClass, UmlInterface, UmlDataType, UmlEnumeration]] = None
    parameters: List[UmlParameter] = field(default_factory=list)
    visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC
    is_static: Optional[bool] = None
    is_ordered: Optional[bool] = None
    is_unique: Optional[bool] = None
    is_query: Optional[bool] = None
    is_derived: Optional[bool] = None
    is_derived_union: Optional[bool] = None
    is_abstract: bool = False
    exceptions: List[str] = field(default_factory=list)

    @property
    def return_type(self) -> Optional[Union[UmlPrimitiveType, UmlClass, UmlInterface, UmlDataType, UmlEnumeration]]:
        return self._return_type

    @return_type.setter
    def return_type(self, new_return_type: Optional[Union[UmlPrimitiveType, UmlClass, UmlInterface, UmlDataType, UmlEnumeration]]):
        self._return_type = new_return_type
        if self.builder:
            self.builder.register_if_not_present(new_return_type)

    @property
    def parameters(self) -> List[UmlParameter]:
        return self._parameters

    @parameters.setter
    def parameters(self, new_parameters: List[UmlParameter]):
        self._parameters = new_parameters
        if self.builder:
            for param in new_parameters:
                self.builder.register_if_not_present(param)

    @property
    def exceptions(self) -> List[str]:
        return self._exceptions
    
    @exceptions.setter
    def exceptions(self, new_exceptions: List[str]) -> None:
        self._exceptions = new_exceptions



# Relationships

@dataclass(kw_only=True)
class UmlAssociationEnd(IUmlAssociationEnd, UmlElement, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlAssociationEnd'
    element: UmlClassifier
    role: Optional[str] = None
    multiplicity: UmlMultiplicityEnum = UmlMultiplicityEnum.ONE
    navigability: bool = True
    aggregation_kind: Optional[str] = None

    @property
    def element(self) -> UmlClassifier:
        return self._end
    
    @element.setter
    def element(self, new_end: UmlClassifier):
        self._end = new_end
        if self.builder:
            self.builder.register_if_not_present(new_end)


@dataclass(kw_only=True)
class UmlAssociationBase(IUmlAssociationBase, UmlElement):
    end1: UmlAssociationEnd
    end2: UmlAssociationEnd

    def __post_init__(self):
        if self.builder:
            self.end1.builder = self.builder
            self.end2.builder = self.builder
            self.builder.register_if_not_present(self.end1.element)
            self.builder.register_if_not_present(self.end2.element)


@dataclass(kw_only=True)
class UmlAssociation(UmlAssociationBase, metaclass=property_wizard):
    """
    Standard (bi-directional) association.
    """
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlAssociation'
    direction: UmlAssociationDirectionEnum = UmlAssociationDirectionEnum.BIDIRECTIONAL

    @property
    def end1(self) -> UmlAssociationEnd:
        return self._end1
    
    @end1.setter
    def end1(self, new_end1: UmlAssociationEnd):
        self._end1 = new_end1
        if self.builder:
            new_end1.builder = self.builder
            self.builder.register_if_not_present(new_end1.element)

    @property
    def end2(self) -> UmlAssociationEnd:
        return self._end2
    
    @end2.setter
    def end2(self, new_end2: UmlAssociationEnd):
        self._end2 = new_end2
        if self.builder:
            new_end2.builder = self.builder
            self.builder.register_if_not_present(new_end2.element)


@dataclass(kw_only=True)
class UmlDirectedAssociation(UmlAssociationBase, metaclass=property_wizard):
    """
    Directed association.
    """
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlDirectedAssociation'
    direction: UmlAssociationDirectionEnum = UmlAssociationDirectionEnum.DIRECTED

    @property
    def source(self) -> UmlAssociationEnd:
        return self._end1
    
    @source.setter
    def source(self, new_source: UmlAssociationEnd):
        self._end1 = new_source
        if self.builder:
            new_source.builder = self.builder
            self.builder.register_if_not_present(new_source.element)

    @property
    def target(self) -> UmlAssociationEnd:
        return self._end2
    
    @target.setter
    def target(self, new_target: UmlAssociationEnd):
        self._end2 = new_target
        if self.builder:
            new_target.builder = self.builder
            self.builder.register_if_not_present(new_target.element)


@dataclass(kw_only=True)
class UmlAggregation(UmlDirectedAssociation, IUmlAggregation, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlAggregation'


@dataclass(kw_only=True)
class UmlComposition(UmlDirectedAssociation, IUmlComposition, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlComposition'


@dataclass(kw_only=True)
class UmlRealization(UmlDirectedAssociation, IUmlRealization, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlRealization'

@dataclass(kw_only=True)
class UmlGeneralization(UmlElement, IUmlGeneralization, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlGeneralization'
    specific: UmlClass
    general: UmlClass

    @property
    def source(self) -> UmlClass:
        return self.specific
    
    @source.setter
    def source(self, new_source: UmlClass):
        self.specific = new_source
    
    @property
    def target(self) -> UmlClass:
        return self.general

    @target.setter
    def target(self, new_target: UmlClass):
        self.general = new_target

    @property
    def specific(self) -> UmlClass:
        return self._specific

    @specific.setter
    def specific(self, new_specific: UmlClass):
        self._specific = new_specific
        if self.builder:
            self.builder.register_if_not_present(new_specific)

    @property
    def general(self) -> UmlClass:
        return self._general

    @general.setter
    def general(self, new_general: UmlClass):
        self._general = new_general
        if self.builder:
            self.builder.register_if_not_present(new_general)


@dataclass(kw_only=True)
class UmlDependency(IUmlDependency, UmlElement, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlDependency'
    client: UmlClassifier
    supplier: UmlClassifier

    @property
    def source(self) -> UmlClassifier:
        return self.client
    
    @source.setter
    def source(self, new_source: UmlClassifier):
        self.client = new_source

    @property
    def target(self) -> UmlClassifier:
        return self.supplier
    
    @target.setter
    def target(self, new_target: UmlClassifier):
        self.supplier = new_target

    @property
    def client(self) -> UmlClassifier:
        return self._client

    @client.setter
    def client(self, new_client: UmlClassifier):
        self._client = new_client
        if self.builder:
            self.builder.register_if_not_present(new_client)

    @property
    def supplier(self) -> UmlClassifier:
        return self._supplier

    @supplier.setter
    def supplier(self, new_supplier: UmlClassifier):
        self._supplier = new_supplier
        if self.builder:
            self.builder.register_if_not_present(new_supplier)


# Interaction Elements
@dataclass(kw_only=True)
class UmlLifeline(IUmlLifeline, UmlNamedElement, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlLifeline'
    represents: UmlClass
    fragments: List['UmlFragment'] = field(default_factory=list)

    @property
    def represents(self) -> UmlClass:
        return self._represents
    
    @represents.setter
    def represents(self, new_represents: UmlClass):
        self._represents = new_represents
        if self.builder:
            self.builder.register_if_not_present(new_represents)

    @property
    def fragments(self) -> List['UmlFragment']:
        return self._fragments
    
    @fragments.setter
    def fragments(self, new_fragments: List['UmlFragment']):
        self._fragments = new_fragments
        if self.builder:
            for fragment in new_fragments:
                self.builder.register_if_not_present(fragment)


@dataclass(kw_only=True)
class UmlMessage(IUmlMessage, UmlElement, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlMessage'
    sender: UmlLifeline
    receiver: UmlLifeline
    message_type: Optional[str] = None
    content: Optional[str] = None

    @property
    def sender(self) -> UmlLifeline:
        return self._sender
    
    @sender.setter
    def sender(self, new_sender: UmlLifeline):
        self._sender = new_sender
        if self.builder:
            self.builder.register_if_not_present(new_sender)

    @property
    def receiver(self) -> UmlLifeline:
        return self._receiver

    @receiver.setter
    def receiver(self, new_receiver: UmlLifeline):
        self._receiver = new_receiver
        if self.builder:
            self.builder.register_if_not_present(new_receiver)



@dataclass(kw_only=True)
class UmlFragment(IUmlFragment, UmlElement, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlFragment'
    covered_lifelines: List[UmlLifeline] = field(default_factory=list)
    covered_messages: List[UmlMessage] = field(default_factory=list)


@dataclass(kw_only=True)
class UmlInteractionOperand(IUmlInteractionOperand, UmlFragment, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlInteractionOperand'
    guard: Optional[str] = None


@dataclass(kw_only=True)
class UmlInteraction(IUmlInteraction, UmlElement, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlInteraction'
    lifelines: List[UmlLifeline] = field(default_factory=list)
    messages: List[UmlMessage] = field(default_factory=list)
    fragments: List[UmlFragment] = field(default_factory=list)

    @property
    def lifelines(self) -> List[UmlLifeline]:
        return self._lifelines

    @lifelines.setter
    def lifelines(self, new_lifelines: List[UmlLifeline]):
        self._lifelines = new_lifelines
        if self.builder:
            for lifeline in new_lifelines:
                self.builder.register_if_not_present(lifeline)

    @property
    def messages(self) -> List[UmlMessage]:
        return self._messages

    @messages.setter
    def messages(self, new_messages: List[UmlMessage]):
        self._messages = new_messages
        if self.builder:
            for message in new_messages:
                self.builder.register_if_not_present(message)

    @property
    def fragments(self) -> List[UmlFragment]:
        return self._fragments
    
    @fragments.setter
    def fragments(self, new_fragments: List[UmlFragment]):
        self._fragments = new_fragments
        if self.builder:
            for fragment in new_fragments:
                self.builder.register_if_not_present(fragment)


@dataclass(kw_only=True)
class UmlPackage(IUmlPackage, UmlNamedElement, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]] = 'UmlPackage'
    packaged_elements: List[UmlElement] = field(default_factory=list, repr=False)
    visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC


    @property
    def packaged_elements(self) -> List[UmlElement]:
        return self._packaged_elements

    @packaged_elements.setter
    def packaged_elements(self, new_packaged_elements: List[UmlElement]):
        self._packaged_elements = new_packaged_elements
        if self.builder:
            for element in new_packaged_elements:
                self.builder.register_if_not_present(element)
