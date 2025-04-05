from enum import Enum

from umlars_translator.core.model.constants import (
    UmlPrimitiveTypeKindEnum,
    UmlDiagramType,
    UmlElementType,
    UmlMultiplicityEnum,
    UmlInteractionOperatorEnum,
    UmlMessageSortEnum
)
from umlars_translator.core.configuration.config_namespace import ConfigNamespace


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
        "refers_to": "refersTo",
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
        "owned_views": "ownedViews",
        "model": "model",
        "messages": "messages",
        "participants": "participants",
        "fragments": "fragments",
        "message_sort": "messageSort",
        "represent": "represent",
        "signature": "signature",
        "operator": "interactionOperator",
        "guard": "guard",
        "operands": "operands",
    }

    MULTIPLICITY_MAPPING: dict[str, str] = {
        "*": UmlMultiplicityEnum.ZERO_OR_MORE.value,
        "0..1": UmlMultiplicityEnum.ZERO_OR_ONE.value,
        "1": UmlMultiplicityEnum.ONE.value,
        "1..*": UmlMultiplicityEnum.ONE_OR_MORE.value,
    }

    PRIMITIVE_TYPE_MAPPING: dict[str, UmlPrimitiveTypeKindEnum] = {
        "String": UmlPrimitiveTypeKindEnum.STRING,
        "Integer": UmlPrimitiveTypeKindEnum.INTEGER,
        "Float": UmlPrimitiveTypeKindEnum.FLOAT,
        "Char": UmlPrimitiveTypeKindEnum.CHAR,
        "Boolean": UmlPrimitiveTypeKindEnum.BOOLEAN,
        "Real": UmlPrimitiveTypeKindEnum.REAL,
        "UnlimitedNatural": UmlPrimitiveTypeKindEnum.UNLIMITED_NATURAL,
        "Void": UmlPrimitiveTypeKindEnum.VOID,
        "Any": UmlPrimitiveTypeKindEnum.ANY,
    }

    MESSAGE_SORT_MAPPING: dict[str, UmlMessageSortEnum] = {
        "synchCall": UmlMessageSortEnum.SYNCH_CALL,
        "asynchCall": UmlMessageSortEnum.ASYNCH_CALL,
        "asynchSignal": UmlMessageSortEnum.ASYNCH_CALL,
        "createMessage": UmlMessageSortEnum.CREATE,
        "deleteMessage": UmlMessageSortEnum.DELETE,
        "returnMessage": UmlMessageSortEnum.REPLY,
    }

    COMBINED_FRAGMENT_OPERATOR_MAPPING: dict[str, UmlInteractionOperatorEnum] = {
        "alt": UmlInteractionOperatorEnum.ALT,
        "opt": UmlInteractionOperatorEnum.OPT,
        "par": UmlInteractionOperatorEnum.PAR,
        "loop": UmlInteractionOperatorEnum.LOOP,
        "break": UmlInteractionOperatorEnum.BREAK,
        "neg": UmlInteractionOperatorEnum.NEG,
        "assert": UmlInteractionOperatorEnum.ASSERT,
        "ignore": UmlInteractionOperatorEnum.IGNORE,
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
        
