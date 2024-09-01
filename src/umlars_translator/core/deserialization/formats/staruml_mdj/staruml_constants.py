from enum import Enum

from src.umlars_translator.core.model.constants import (
    UmlPrimitiveTypeKindEnum,
    UmlDiagramType,
    UmlElementType,
)
from src.umlars_translator.core.configuration.config_namespace import ConfigNamespace


class StarumlMDJConfig(ConfigNamespace):
    KEYS: dict[str, str] = {
        "owned_elements": "ownedElements",
    }

    EA_DIAGRAMS_TYPES_MAPPING: dict[str, str] = {
        "Logical": UmlDiagramType.CLASS,
        "Sequence": UmlDiagramType.SEQUENCE,
    }

    EA_TYPE_ATTRIBUTE_MAPPING: dict[str, str] = {
        "uml:PrimitiveType": UmlElementType.PRIMITIVE_TYPE,
        "uml:Class": UmlElementType.CLASS,
        "uml:Interface": UmlElementType.INTERFACE,
        "uml:Association": UmlElementType.ASSOCIATION,
        "uml:Dependency": UmlElementType.DEPENDENCY,
        "uml:Generalization": UmlElementType.GENERALIZATION,
        "uml:Realization": UmlElementType.REALIZATION,
        "uml:LiteralInteger": UmlPrimitiveTypeKindEnum.INTEGER,
        "uml:LiteralUnlimitedNatural": UmlPrimitiveTypeKindEnum.INTEGER,
        "EAnone_void": None,
        "EAJava_boolean": UmlPrimitiveTypeKindEnum.BOOLEAN,
        "EAJava_void": None,
        "EAJava_int": UmlPrimitiveTypeKindEnum.INTEGER,
        "EAJava_float": UmlPrimitiveTypeKindEnum.FLOAT,
        "EAJava_char": UmlPrimitiveTypeKindEnum.CHAR,
    }

    EA_HREF_ATTRIBUTE_MAPPING: dict[str, str] = {
        "http://schema.omg.org/spec/UML/2.1/uml.xml#Integer": UmlPrimitiveTypeKindEnum.INTEGER,
    }

    # TODO: move to file with non-parsed constants /enums
    class EaPackagedElementTypes(str, Enum):
        """
        String enum is used to allow comparison with xml data.
        """

        PACKAGE = "uml:Package"
        CLASS = "uml:Class"
        INTERFACE = "uml:Interface"
        ASSOCIATION = "uml:Association"
        DEPENDENCY = "uml:Dependency"
        GENERALIZATION = "uml:Generalization"
        REALIZATION = "uml:Realization"
        DATA_TYPE = "uml:DataType"
        ENUMERATION = "uml:Enumeration"
        
