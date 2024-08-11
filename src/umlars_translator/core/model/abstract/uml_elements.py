from abc import ABC, abstractmethod
from typing import List, Optional, Union, ClassVar

from src.umlars_translator.core.model.abstract.uml_model_builder import IUmlModelBuilder
from src.umlars_translator.core.model.abstract.uml_model import IUmlModel
from src.umlars_translator.core.model.constants import UmlPrimitiveTypeTypes, UmlVisibilityEnum, UmlMultiplicityEnum, UmlAssoctioationDirectionEnum


# Base and Common Elements
class IUmlElement(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @property
    @abstractmethod
    def builder(self) -> Optional['IUmlModelBuilder']:
        pass

    @property
    @abstractmethod
    def model(self) -> Optional['IUmlModel']:
        pass


class IUmlNamedElement(IUmlElement):
    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        pass


# Primitive Types
class IUmlPrimitiveType(IUmlNamedElement):
    @property
    @abstractmethod
    def kind(self) -> UmlPrimitiveTypeTypes:
        pass


# Classifiers
class IUmlClassifier(IUmlNamedElement):
    @property
    @abstractmethod
    def visibility(self) -> UmlVisibilityEnum:
        pass

    @property
    @abstractmethod
    def attributes(self) -> List['IUmlAttribute']:
        pass

    @property
    @abstractmethod
    def operations(self) -> List['IUmlOperation']:
        pass


class IUmlClass(IUmlClassifier):
    @property
    @abstractmethod
    def super_classes(self) -> List['IUmlGeneralization']:
        pass

    @property
    @abstractmethod
    def interfaces(self) -> List['IUmlInterface']:
        pass


class IUmlInterface(IUmlClassifier):
    pass


class IUmlDataType(IUmlClassifier):
    pass


class IUmlEnumeration(IUmlNamedElement):
    @property
    @abstractmethod
    def literals(self) -> List[str]:
        pass


# Attributes and Operations
class IUmlAttribute(IUmlNamedElement):
    @property
    @abstractmethod
    def type(self) -> Union[IUmlPrimitiveType, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration]:
        pass

    @property
    @abstractmethod
    def visibility(self) -> UmlVisibilityEnum:
        pass

    @property
    @abstractmethod
    def is_static(self) -> Optional[bool]:
        pass

    @property
    @abstractmethod
    def is_ordered(self) -> Optional[bool]:
        pass

    @property
    @abstractmethod
    def is_unique(self) -> Optional[bool]:
        pass

    @property
    @abstractmethod
    def is_read_only(self) -> Optional[bool]:
        pass

    @property
    @abstractmethod
    def is_query(self) -> Optional[bool]:
        pass

    @property
    @abstractmethod
    def is_derived(self) -> Optional[bool]:
        pass

    @property
    @abstractmethod
    def is_derived_union(self) -> Optional[bool]:
        pass


class IUmlParameter(IUmlNamedElement):
    @property
    @abstractmethod
    def type(self) -> Union[IUmlPrimitiveType, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration]:
        pass


class IUmlOperation(IUmlNamedElement):
    @property
    @abstractmethod
    def return_type(self) -> Optional[Union[IUmlPrimitiveType, IUmlClass, IUmlInterface, IUmlDataType, IUmlEnumeration]]:
        pass

    @property
    @abstractmethod
    def parameters(self) -> List[IUmlParameter]:
        pass

    @property
    @abstractmethod
    def visibility(self) -> UmlVisibilityEnum:
        pass

    @property
    @abstractmethod
    def is_static(self) -> Optional[bool]:
        pass

    @property
    @abstractmethod
    def is_ordered(self) -> Optional[bool]:
        pass

    @property
    @abstractmethod
    def is_unique(self) -> Optional[bool]:
        pass

    @property
    @abstractmethod
    def is_query(self) -> Optional[bool]:
        pass

    @property
    @abstractmethod
    def is_derived(self) -> Optional[bool]:
        pass

    @property
    @abstractmethod
    def is_derived_union(self) -> Optional[bool]:
        pass

    @property
    @abstractmethod
    def is_abstract(self) -> bool:
        pass

    @property
    @abstractmethod
    def exceptions(self) -> List[str]:
        pass


# Relationships
class IUmlGeneralization(IUmlElement):
    @property
    @abstractmethod
    def specific(self) -> IUmlClass:
        pass

    @property
    @abstractmethod
    def general(self) -> IUmlClass:
        pass


class IUmlDependency(IUmlElement):
    @property
    @abstractmethod
    def client(self) -> IUmlClassifier:
        pass

    @property
    @abstractmethod
    def supplier(self) -> IUmlClassifier:
        pass


class IUmlAssociationEnd(IUmlElement):
    @property
    @abstractmethod
    def end(self) -> IUmlClassifier:
        pass

    @property
    @abstractmethod
    def role(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def multiplicity(self) -> UmlMultiplicityEnum:
        pass

    @property
    @abstractmethod
    def navigability(self) -> bool:
        pass

    @property
    @abstractmethod
    def visibility(self) -> UmlVisibilityEnum:
        pass

    @property
    @abstractmethod
    def aggregation_kind(self) -> Optional[str]:
        pass


class IUmlOwnedEnd(IUmlAssociationEnd):
    pass


class IUmlMemberEnd(IUmlAssociationEnd):
    pass


class IUmlAssociationBase(IUmlElement):
    ASSOCIATION_DIRECTION: ClassVar[UmlAssoctioationDirectionEnum]

    @property
    @abstractmethod
    def end1(self) -> Union[IUmlOwnedEnd, IUmlMemberEnd]:
        pass

    @property
    @abstractmethod
    def end2(self) -> Union[IUmlOwnedEnd, IUmlMemberEnd]:
        pass


    @classmethod
    def association_direction(cls) -> UmlAssoctioationDirectionEnum:
        return cls.ASSOCIATION_DIRECTION


class IUmlAssociation(IUmlAssociationBase):
    """
    Standard Association - Bidirectional
    """
    ASSOCIATION_DIRECTION = UmlAssoctioationDirectionEnum.BIDIRECTIONAL


class IUmlDirectedAssociation(IUmlAssociationBase):
    ASSOCIATION_DIRECTION = UmlAssoctioationDirectionEnum.DIRECTED

    def end1(self) -> Union[IUmlOwnedEnd, IUmlMemberEnd]:
        self.source

    def end2(self) -> Union[IUmlOwnedEnd, IUmlMemberEnd]:
        self.target

    @property
    @abstractmethod
    def source(self) -> Union[IUmlOwnedEnd, IUmlMemberEnd]:
        pass

    @property
    @abstractmethod
    def target(self) -> Union[IUmlOwnedEnd, IUmlMemberEnd]:
        pass


class IUmlAggregation(IUmlDirectedAssociation):
    pass


class IUmlComposition(IUmlDirectedAssociation):
    pass


class IUmlRealization(IUmlDirectedAssociation):
    pass


# Interaction Elements
class IUmlLifeline(IUmlNamedElement):
    @property
    @abstractmethod
    def represents(self) -> IUmlClass:
        pass


class IUmlMessage(IUmlElement):
    @property
    @abstractmethod
    def sender(self) -> IUmlLifeline:
        pass

    @property
    @abstractmethod
    def receiver(self) -> IUmlLifeline:
        pass

    @property
    @abstractmethod
    def message_type(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def content(self) -> Optional[str]:
        pass


class IUmlFragment(IUmlElement):
    @property
    @abstractmethod
    def covered_lifelines(self) -> List[IUmlLifeline]:
        pass

    @property
    @abstractmethod
    def covered_messages(self) -> List[IUmlMessage]:
        pass


class IUmlInteractionOperand(IUmlFragment):
    @property
    @abstractmethod
    def guard(self) -> Optional[str]:
        pass


class IUmlInteraction(IUmlElement):
    @property
    @abstractmethod
    def lifelines(self) -> List[IUmlLifeline]:
        pass

    @property
    @abstractmethod
    def messages(self) -> List[IUmlMessage]:
        pass

    @property
    @abstractmethod
    def fragments(self) -> List[IUmlFragment]:
        pass


class IUmlPackage(IUmlNamedElement):
    @property
    @abstractmethod
    def packaged_elements(self) -> List[IUmlElement]:
        pass
