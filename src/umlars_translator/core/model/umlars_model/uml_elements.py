from dataclasses import dataclass, field
from typing import List, Optional, Union, ClassVar, TYPE_CHECKING
from enum import Enum
import uuid

from dataclass_wizard import property_wizard, JSONWizard
from src.umlars_translator.core.model.umlars_model.uml_model_builder import UmlModelBuilder
if TYPE_CHECKING:
    from src.umlars_translator.core.model.umlars_model.uml_model import UmlModel


@dataclass
class UmlElement(JSONWizard, metaclass=property_wizard):
    __ELEMENT_NAME: ClassVar[Optional[str]]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    builder: Optional['UmlModelBuilder'] = field(default=None, repr=False, init=True)
    model: Optional['UmlModel'] = field(default=None, repr=False, init=True)

    @classmethod
    def element_name(cls) -> str:
        try:
            return cls.__ELEMENT_NAME
        except AttributeError:
            return cls.__name__


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id: str) -> None:
        old_id = self._id
        self._id = new_id
        if self.builder:
            self.builder.register_if_not_present(self, old_id)

    @property
    def builder(self) -> Optional['UmlModelBuilder']:
        return self._builder if self._builder else self._model.builder

    @builder.setter
    def builder(self, new_builder: 'UmlModelBuilder'):
        self._builder = new_builder


@dataclass
class UmlNamedElement(UmlElement):
    name: Optional[str] = None

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, new_name: Optional[str]):
        self._name = new_name


class VisibilityEnum(str, Enum):
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


@dataclass
class UmlPrimitiveType(UmlNamedElement):
    kind: UmlPrimitiveTypeEnum

    @property
    def kind(self) -> UmlPrimitiveTypeEnum:
        return self._kind

    @kind.setter
    def kind(self, new_kind: UmlPrimitiveTypeEnum):
        self._kind = new_kind


# Classifiers
@dataclass
class Classifier(UmlNamedElement):
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


@dataclass
class UmlClass(Classifier):
    super_classes: List['UmlGeneralization'] = field(default_factory=list)
    interfaces: List['Interface'] = field(default_factory=list)

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
    def interfaces(self) -> List['Interface']:
        return self._interfaces

    @interfaces.setter
    def interfaces(self, new_interfaces: List['Interface']):
        self._interfaces = new_interfaces
        if self.builder:
            for interface in new_interfaces:
                self.builder.register_if_not_present(interface)


@dataclass
class Interface(Classifier):
    pass


@dataclass
class DataType(Classifier):
    pass


@dataclass
class Enumeration(UmlNamedElement):
    literals: List[str] = field(default_factory=list)

    @property
    def literals(self) -> List[str]:
        return self._literals

    @literals.setter
    def literals(self, new_literals: List[str]):
        self._literals = new_literals


# Attributes and Operations
@dataclass
class UmlAttribute(UmlNamedElement):
    type: Union[UmlPrimitiveType, UmlClass, Interface, DataType, Enumeration]
    visibility: VisibilityEnum = VisibilityEnum.PUBLIC
    is_static: bool = False

    @property
    def type(self) -> Union[UmlPrimitiveType, UmlClass, Interface, DataType, Enumeration]:
        return self._type

    @type.setter
    def type(self, new_type: Union[UmlPrimitiveType, UmlClass, Interface, DataType, Enumeration]):
        self._type = new_type
        if self.builder:
            self.builder.register_if_not_present(new_type)


@dataclass
class UmlParameter(UmlNamedElement):
    type: Union[UmlPrimitiveType, UmlClass, Interface, DataType, Enumeration]

    @property
    def type(self) -> Union[UmlPrimitiveType, UmlClass, Interface, DataType, Enumeration]:
        return self._type

    @type.setter
    def type(self, new_type: Union[UmlPrimitiveType, UmlClass, Interface, DataType, Enumeration]):
        self._type = new_type
        if self.builder:
            self.builder.register_if_not_present(new_type)


@dataclass
class UmlOperation(UmlNamedElement):
    return_type: Optional[Union[UmlPrimitiveType, UmlClass, Interface, DataType, Enumeration]] = None
    parameters: List[UmlParameter] = field(default_factory=list)
    visibility: VisibilityEnum = VisibilityEnum.PUBLIC
    is_static: bool = False
    is_abstract: bool = False
    exceptions: List[str] = field(default_factory=list)

    @property
    def return_type(self) -> Optional[Union[UmlPrimitiveType, UmlClass, Interface, DataType, Enumeration]]:
        return self._return_type

    @return_type.setter
    def return_type(self, new_return_type: Optional[Union[UmlPrimitiveType, UmlClass, Interface, DataType, Enumeration]]):
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
@dataclass
class UmlGeneralization(UmlElement):
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


@dataclass
class UmlDependency(UmlElement):
    client: Classifier
    supplier: Classifier

    @property
    def client(self) -> Classifier:
        return self._client

    @client.setter
    def client(self, new_client: Classifier):
        self._client = new_client
        if self.builder:
            self.builder.register_if_not_present(new_client)

    @property
    def supplier(self) -> Classifier:
        return self._supplier

    @supplier.setter
    def supplier(self, new_supplier: Classifier):
        self._supplier = new_supplier
        if self.builder:
            self.builder.register_if_not_present(new_supplier)


@dataclass
class UmlAssociationEnd(UmlElement):
    end: Classifier
    role: Optional[str] = None
    multiplicity: UmlMultiplicityEnum = UmlMultiplicityEnum.ONE
    navigability: bool = True
    visibility: VisibilityEnum = VisibilityEnum.PUBLIC
    aggregation_kind: Optional[str] = None


@dataclass
class UmlOwnedEnd(UmlAssociationEnd):
    pass


@dataclass
class UmlMemberEnd(UmlAssociationEnd):
    pass


class AssociationTypeEnum(str, Enum):
    ASSOCIATION = "association"
    AGGREGATION = "aggregation"
    COMPOSITION = "composition"


@dataclass
class UmlAssociationBase(UmlElement):
    end1: Union[UmlOwnedEnd, UmlMemberEnd]
    end2: Union[UmlOwnedEnd, UmlMemberEnd]
    association_type: AssociationTypeEnum = AssociationTypeEnum.ASSOCIATION

    def __post_init__(self):
        if self.builder:
            self.end1.builder = self.builder
            self.end2.builder = self.builder
            self.builder.register_if_not_present(self.end1)
            self.builder.register_if_not_present(self.end2)


@dataclass
class UmlAggregation(UmlAssociationBase):
    aggregation_type: AssociationTypeEnum = AssociationTypeEnum.AGGREGATION


@dataclass
class UmlComposition(UmlAssociationBase):
    composition_type: AssociationTypeEnum = AssociationTypeEnum.COMPOSITION


# Interaction Elements
@dataclass
class UmlLifeline(UmlNamedElement):
    represents: UmlClass


@dataclass
class UmlMessage(UmlElement):
    sender: UmlLifeline
    receiver: UmlLifeline
    message_type: str
    content: str


@dataclass
class UmlInteraction(UmlElement):
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


@dataclass
class UmlPackage(UmlNamedElement):
    packaged_elements: List[UmlElement] = field(default_factory=list)

    @property
    def packaged_elements(self) -> List[UmlElement]:
        return self._packaged_elements

    @packaged_elements.setter
    def packaged_elements(self, new_packaged_elements: List[UmlElement]):
        self._packaged_elements = new_packaged_elements
        if self.builder:
            for element in new_packaged_elements:
                self.builder.register_if_not_present(element)
