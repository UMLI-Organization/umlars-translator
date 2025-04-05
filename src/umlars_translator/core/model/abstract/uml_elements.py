from abc import ABC, abstractmethod
from typing import List, Optional, Union, ClassVar, TYPE_CHECKING


if TYPE_CHECKING:
    from umlars_translator.core.model.abstract.uml_model_builder import IUmlModelBuilder
    from umlars_translator.core.model.abstract.uml_model import IUmlModel

from umlars_translator.core.model.constants import UmlPrimitiveTypeKindEnum, UmlAssociationTypeEnum, UmlVisibilityEnum, UmlMultiplicityEnum, UmlAssociationDirectionEnum, UmlParameterDirectionEnum, UmlInteractionOperatorEnum, UmlMessageSortEnum, UmlMessageKindEnum
from umlars_translator.core.utils.visitor import IVisitable, IVisitor


# Base and Common Elements
class IUmlElement(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        ...

    @property
    @abstractmethod
    def builder(self) -> Optional['IUmlModelBuilder']:
        ...

    @property
    @abstractmethod
    def model(self) -> Optional['IUmlModel']:
        ...


class IUmlNamedElement(IUmlElement):
    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        ...

    @property
    @abstractmethod
    def visibility(self) -> UmlVisibilityEnum:
        ...


# Primitive Types
class IUmlPrimitiveType(IUmlNamedElement):
    @property
    @abstractmethod
    def kind(self) -> UmlPrimitiveTypeKindEnum:
        ...


# Classifiers
class IUmlClassifier(IUmlNamedElement):
    @property
    @abstractmethod
    def attributes(self) -> List['IUmlAttribute']:
        ...

    @property
    @abstractmethod
    def operations(self) -> List['IUmlOperation']:
        ...


class IUmlClass(IUmlClassifier):
    @property
    @abstractmethod
    def generalizations(self) -> List['IUmlGeneralization']:
        ...

    @property
    @abstractmethod
    def interfaces(self) -> List['IUmlInterface']:
        ...


class IUmlInterface(IUmlClassifier):
    ...


class IUmlDataType(IUmlClassifier):
    ...


class IUmlEnumeration(IUmlNamedElement):
    @property
    @abstractmethod
    def literals(self) -> List[str]:
        ...


# Attributes and Operations
class IUmlAttribute(IUmlNamedElement):
    @property
    @abstractmethod
    def type(self) -> Union[IUmlPrimitiveType, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration]:
        ...

    @property
    @abstractmethod
    def is_static(self) -> Optional[bool]:
        ...

    @property
    @abstractmethod
    def is_ordered(self) -> Optional[bool]:
        ...

    @property
    @abstractmethod
    def is_unique(self) -> Optional[bool]:
        ...

    @property
    @abstractmethod
    def is_read_only(self) -> Optional[bool]:
        ...

    @property
    @abstractmethod
    def is_query(self) -> Optional[bool]:
        ...

    @property
    @abstractmethod
    def is_derived(self) -> Optional[bool]:
        ...

    @property
    @abstractmethod
    def is_derived_union(self) -> Optional[bool]:
        ...


class IUmlParameter(IUmlNamedElement):
    @property
    @abstractmethod
    def type(self) -> Union[IUmlPrimitiveType, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration]:
        ...

    @property
    @abstractmethod
    def direction(self) -> UmlParameterDirectionEnum:
        ...


class IUmlOperation(IUmlNamedElement):
    @property
    @abstractmethod
    def return_type(self) -> Optional[Union[IUmlPrimitiveType, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration]]:
        ...

    @property
    @abstractmethod
    def parameters(self) -> List[IUmlParameter]:
        ...

    @property
    @abstractmethod
    def visibility(self) -> UmlVisibilityEnum:
        ...

    @property
    @abstractmethod
    def is_static(self) -> Optional[bool]:
        ...

    @property
    @abstractmethod
    def is_ordered(self) -> Optional[bool]:
        ...

    @property
    @abstractmethod
    def is_unique(self) -> Optional[bool]:
        ...

    @property
    @abstractmethod
    def is_query(self) -> Optional[bool]:
        ...

    @property
    @abstractmethod
    def is_derived(self) -> Optional[bool]:
        ...

    @property
    @abstractmethod
    def is_derived_union(self) -> Optional[bool]:
        ...

    @property
    @abstractmethod
    def is_abstract(self) -> bool:
        ...

    @property
    @abstractmethod
    def exceptions(self) -> List[str]:
        ...


# Relationships
class IUmlGeneralization(IUmlElement):
    @property
    @abstractmethod
    def specific(self) -> IUmlClass:
        ...

    @property
    @abstractmethod
    def general(self) -> IUmlClass:
        ...


class IUmlDependency(IUmlElement):
    @property
    @abstractmethod
    def client(self) -> IUmlClassifier:
        ...

    @property
    @abstractmethod
    def supplier(self) -> IUmlClassifier:
        ...


class IUmlRealization(IUmlDependency):
    ...


class IUmlAssociationEnd(IUmlNamedElement):
    @property
    @abstractmethod
    def element(self) -> IUmlClassifier:
        ...

    @property
    @abstractmethod
    def role(self) -> Optional[str]:
        ...

    @property
    @abstractmethod
    def multiplicity(self) -> UmlMultiplicityEnum:
        ...

    @property
    @abstractmethod
    def navigability(self) -> bool:
        ...


class IUmlAssociationBase(IUmlElement):
    ASSOCIATION_DIRECTION: ClassVar[UmlAssociationDirectionEnum]
    ASSOCIATION_TYPE: ClassVar[UmlAssociationTypeEnum]

    @property
    def type(self) -> UmlAssociationTypeEnum:
        return self.association_type()

    @property
    def direction(self) -> UmlAssociationDirectionEnum:
        return self.association_direction()

    @property
    @abstractmethod
    def end1(self) -> IUmlAssociationEnd:
        ...

    @property
    @abstractmethod
    def end2(self) -> IUmlAssociationEnd:
        ...

    @classmethod
    def association_direction(cls) -> UmlAssociationDirectionEnum:
        return cls.ASSOCIATION_DIRECTION
    
    @classmethod
    def association_type(cls) -> UmlAssociationTypeEnum:
        return cls.ASSOCIATION_TYPE


class IUmlAssociation(IUmlAssociationBase):
    """
    Standard Association - Bidirectional
    """
    ASSOCIATION_DIRECTION = UmlAssociationDirectionEnum.BIDIRECTIONAL
    ASSOCIATION_TYPE = UmlAssociationTypeEnum.ASSOCIATION


class IUmlDirectedAssociation(IUmlAssociationBase):
    ASSOCIATION_DIRECTION = UmlAssociationDirectionEnum.DIRECTED

    @property
    def end1(self) -> IUmlAssociationEnd:
        return self.source

    @property
    def end2(self) -> IUmlAssociationEnd:
        return self.target

    @property
    @abstractmethod
    def source(self) -> IUmlAssociationEnd:
        ...

    @property
    @abstractmethod
    def target(self) -> IUmlAssociationEnd:
        ...


class IUmlAggregation(IUmlDirectedAssociation):
    ASSOCIATION_TYPE = UmlAssociationTypeEnum.AGGREGATION


class IUmlComposition(IUmlDirectedAssociation):
    ASSOCIATION_TYPE = UmlAssociationTypeEnum.COMPOSITION


# Interaction Elements
class IUmlOrderedElement(ABC):
    @property
    @abstractmethod
    def ordering_key(self) -> int:
        ...


class IUmlOccurrenceSpecification(IUmlElement, IUmlOrderedElement):
    @property
    @abstractmethod
    def covered(self) -> "IUmlLifeline":
        ...


class IUmlInteractionUse(IUmlNamedElement, IUmlOrderedElement):
    @property
    @abstractmethod
    def covered(self) -> List["IUmlLifeline"]:
        ...

    @property
    @abstractmethod
    def interaction(self) -> "IUmlInteraction":
        ...


class IUmlCombinedFragment(IUmlNamedElement, IUmlOrderedElement):
    @property
    @abstractmethod
    def operands(self) -> List["IUmlOperand"]:
        ...

    @property
    @abstractmethod
    def covered(self) -> List["IUmlLifeline"]:
        ...

    @property
    @abstractmethod
    def operator(self) -> UmlInteractionOperatorEnum:
        ...


class IUmlOperand(IUmlElement):
    @property
    @abstractmethod
    def guard(self) -> Optional[str]:
        ...

    @property
    @abstractmethod
    def fragments(self) -> List[Union[IUmlOccurrenceSpecification, IUmlInteractionUse, IUmlCombinedFragment]]:
        ...


class IUmlLifeline(IUmlNamedElement):
    @property
    @abstractmethod
    def represents(self) -> Union[IUmlClass, IUmlInterface]:
        ...


class IUmlMessage(IUmlNamedElement):
    @property
    @abstractmethod
    def send_event(self) -> IUmlOccurrenceSpecification:
        ...

    @property
    @abstractmethod
    def receive_event(self) -> IUmlOccurrenceSpecification:
        ...

    @property
    @abstractmethod
    def signature(self) -> Optional[IUmlOperation]:
        ...

    @property
    @abstractmethod
    def arguments(self) -> List[str]:
        ...

    @property
    @abstractmethod
    def sort(self) -> UmlMessageSortEnum:
        ...

    @property
    @abstractmethod
    def kind(self) -> UmlMessageKindEnum:
        ...


class IUmlInteraction(IUmlNamedElement):
    @property
    @abstractmethod
    def lifelines(self) -> List[IUmlLifeline]:
        ...

    @property
    @abstractmethod
    def messages(self) -> List[IUmlMessage]:
        ...

    @property
    @abstractmethod
    def fragments(self) -> List[Union[IUmlOccurrenceSpecification, IUmlInteractionUse, IUmlCombinedFragment]]:
        ...


class IUmlModelElements(IVisitable, ABC):
    def accept(self, visitor: IVisitor):
        return visitor.visit_uml_model_elements(self)
    
    @property
    @abstractmethod
    def classes() -> List[IUmlClass]:
        ...

    @property
    @abstractmethod
    def interfaces() -> List[IUmlInterface]:
        ...

    @property
    @abstractmethod
    def data_types() -> List[IUmlDataType]:
        ...

    @property
    @abstractmethod
    def enumerations() -> List[IUmlEnumeration]:
        ...

    @property
    @abstractmethod
    def primitive_types() -> List[IUmlPrimitiveType]:
        ...

    @property
    @abstractmethod
    def associations() -> List[Union["IUmlAssociation", "IUmlDirectedAssociation"]]:
        ...

    @property
    @abstractmethod
    def generalizations() -> List[IUmlGeneralization]:
        ...

    @property
    @abstractmethod
    def dependencies() -> List[IUmlDependency]:
        ...

    @property
    @abstractmethod
    def realizations() -> List[IUmlRealization]:
        ...

    @property
    @abstractmethod
    def interactions() -> List[IUmlInteraction]:
        ...

    @property
    @abstractmethod
    def packages() -> List["IUmlPackage"]:
        ...


class IUmlPackage(IUmlNamedElement):
    @property
    @abstractmethod
    def elements(self) -> IUmlModelElements:
        ...
