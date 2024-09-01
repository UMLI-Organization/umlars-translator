from enum import Enum

from src.umlars_translator.core.model.constants import (
    UmlPrimitiveTypeKindEnum,
    UmlDiagramType,
    UmlElementType,
    UmlMultiplicityEnum
)
from src.umlars_translator.core.configuration.config_namespace import ConfigNamespace


class StarumlMDJConfig(ConfigNamespace):
    KEYS: dict[str, str] = {
        "id": "_id",
        "name": "name",
        "type": "_type",
        "type_ref": "type",
        "parent_id": "_parent",
        "end1": "end1",
        "end2": "end2",
        "source": "source",
        "target": "target",
        "reference": "reference",
        "multiplicity": "multiplicity",
        "visibility": "visibility",
        "attributes": "attributes",
        "operations": "operations",
        "parameters": "parameters",
        "direction": "direction",
        "owned_elements": "ownedElements",
        "owned_attributes": "attributes",
        "owned_operations": "operations",

    }

    MULTIPLICITY_MAPPING: dict[str, str] = {
        "*": UmlMultiplicityEnum.ZERO_OR_MORE.value,
        "0..1": UmlMultiplicityEnum.ZERO_OR_ONE.value,
        "1": UmlMultiplicityEnum.ONE.value,
        "1..*": UmlMultiplicityEnum.ONE_OR_MORE.value,
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
        
