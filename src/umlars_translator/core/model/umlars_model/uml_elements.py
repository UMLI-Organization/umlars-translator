from dataclasses import dataclass, field
from typing import List, Optional, Union, TYPE_CHECKING
from enum import Enum

from dataclass_wizard import property_wizard

from src.umlars_translator.core.model.umlars_model.uml_element import UmlElement, UmlNamedElement


class UmlVisibilityEnum(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"


class UmlMultiplicityEnum(str, Enum):
    ZERO_OR_ONE = "0..1"
    ONE = "1"
    ZERO_OR_MORE = "0..*"
    ONE_OR_MORE = "1..*"


# Primitive Types
class UmlPrimitiveTypeEnum(str, Enum):
    INTEGER = "int"
    FLOAT = "float"
    STRING = "string"
    BOOLEAN = "boolean"


@dataclass(kw_only=True)
class UmlPrimitiveType(UmlNamedElement, metaclass=property_wizard):
    kind: UmlPrimitiveTypeEnum

    @property
    def kind(self) -> UmlPrimitiveTypeEnum:
        return self._kind

    @kind.setter
    def kind(self, new_kind: UmlPrimitiveTypeEnum):
        self._kind = new_kind


# Classifiers
@dataclass(kw_only=True)
class UmlClassifier(UmlNamedElement, metaclass=property_wizard):
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
class UmlClass(UmlClassifier, metaclass=property_wizard):
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
class UmlInterface(UmlClassifier, metaclass=property_wizard):
    pass


@dataclass(kw_only=True)
class UmlDataType(UmlClassifier, metaclass=property_wizard):
    pass


@dataclass(kw_only=True)
class UmlEnumeration(UmlNamedElement, metaclass=property_wizard):
    literals: List[str] = field(default_factory=list)

    @property
    def literals(self) -> List[str]:
        return self._literals

    @literals.setter
    def literals(self, new_literals: List[str]):
        self._literals = new_literals


# Attributes and Operations
@dataclass(kw_only=True)
class UmlAttribute(UmlNamedElement, metaclass=property_wizard):
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
class UmlParameter(UmlNamedElement, metaclass=property_wizard):
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
class UmlOperation(UmlNamedElement, metaclass=property_wizard):
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


# Relationships
@dataclass(kw_only=True)
class UmlGeneralization(UmlElement, metaclass=property_wizard):
    specific: UmlClass
    general: UmlClass

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
class UmlDependency(UmlElement, metaclass=property_wizard):
    client: UmlClassifier
    supplier: UmlClassifier

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


@dataclass(kw_only=True)
class UmlAssociationEnd(UmlElement, metaclass=property_wizard):
    end: UmlClassifier
    role: Optional[str] = None
    multiplicity: UmlMultiplicityEnum = UmlMultiplicityEnum.ONE
    navigability: bool = True
    visibility: UmlVisibilityEnum = UmlVisibilityEnum.PUBLIC
    aggregation_kind: Optional[str] = None


@dataclass(kw_only=True)
class UmlOwnedEnd(UmlAssociationEnd, metaclass=property_wizard):
    pass


@dataclass(kw_only=True)
class UmlMemberEnd(UmlAssociationEnd, metaclass=property_wizard):
    pass


class AssociationTypeEnum(str, Enum):
    ASSOCIATION = "association"
    AGGREGATION = "aggregation"
    COMPOSITION = "composition"


@dataclass(kw_only=True)
class UmlAssociationBase(UmlElement, metaclass=property_wizard):
    end1: Union[UmlOwnedEnd, UmlMemberEnd]
    end2: Union[UmlOwnedEnd, UmlMemberEnd]
    association_type: AssociationTypeEnum = AssociationTypeEnum.ASSOCIATION

    def __post_init__(self):
        if self.builder:
            self.end1.builder = self.builder
            self.end2.builder = self.builder
            self.builder.register_if_not_present(self.end1)
            self.builder.register_if_not_present(self.end2)


@dataclass(kw_only=True)
class UmlAggregation(UmlAssociationBase, metaclass=property_wizard):
    aggregation_type: AssociationTypeEnum = AssociationTypeEnum.AGGREGATION


@dataclass(kw_only=True)
class UmlComposition(UmlAssociationBase, metaclass=property_wizard):
    composition_type: AssociationTypeEnum = AssociationTypeEnum.COMPOSITION


# Interaction Elements
@dataclass(kw_only=True)
class UmlLifeline(UmlNamedElement, metaclass=property_wizard):
    represents: UmlClass


@dataclass(kw_only=True)
class UmlMessage(UmlElement, metaclass=property_wizard):
    sender: UmlLifeline
    receiver: UmlLifeline
    message_type: Optional[str] = None
    content: Optional[str] = None


@dataclass(kw_only=True)
class UmlFragment(UmlElement, metaclass=property_wizard):
    covered_lifelines: List[UmlLifeline] = field(default_factory=list)
    covered_messages: List[UmlMessage] = field(default_factory=list)
    


@dataclass(kw_only=True)
class UmlInteraction(UmlElement, metaclass=property_wizard):
    lifelines: List[UmlLifeline] = field(default_factory=list)
    messages: List[UmlMessage] = field(default_factory=list)

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


@dataclass(kw_only=True)
class UmlPackage(UmlNamedElement, metaclass=property_wizard):
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
