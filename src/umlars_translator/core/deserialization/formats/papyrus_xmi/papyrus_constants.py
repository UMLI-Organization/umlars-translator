from enum import Enum

from umlars_translator.core.model.constants import (
    UmlPrimitiveTypeKindEnum,
    UmlDiagramType,
    UmlElementType,
)
from umlars_translator.core.configuration.config_namespace import ParsedConfigNamespace


# TODO: split config into parsed config and normal - so u can use normal enums etc and get IDE suggestions


class PapyrusXmiConfig(ParsedConfigNamespace):
    # TODO: use to check if namespace is allowed for data source
    ALLOWED_NAMESPACES: dict[str, list] = {
        "uml": ["{http://schema.omg.org/spec/UML/2.1}"],
        "xmi": ["{http://schema.omg.org/spec/XMI/2.1}"],
    }

    TAGS: dict[str, str] = {
        "root": "{{{xmi}}}XMI",
        "model": "{{{uml}}}Model",
        "owned_end": "ownedEnd",
        "end_type": "type",
        "owned_attribute": "ownedAttribute",
        "sequence_behavior": "ownedBehavior",
        "attribute_type": "type",
        "owned_operation": "ownedOperation",
        "operation_parameter": "ownedParameter",
        "type": "type",
        "property_type": "type",
        "covered": "covered",
        "operand": "operand",
        "guard": "guard",
        "specification": "specification",
        "properties": "properties",
        "elements": "elements",
        "element": "element",
        "packaged_element": "packagedElement",
        "lifeline": "lifeline",
        "fragment": "fragment",
        "message": "message",
        "lower_value": "lowerValue",
        "upper_value": "upperValue",
    }

    ATTRIBUTES: dict[str, str] = {
        "id": "{{{xmi}}}id",
        "type": "{{{xmi}}}type",
        "xmi_version": "{{{xmi}}}version",
        "uml_namespace": "{{{uml}}}uml",
        "exporter": "exporter",
        "exporterVersion": "exporterVersion",
        "exporterID": "exporterID",
        "name": "name",
        "idref": "{{{xmi}}}idref",
        "member_end": "memberEnd",
        "href": "href",
        "visibility": "visibility",
        "lower_value": "value",
        "upper_value": "value",
        "message_kind": "messageKind",
        "message_sort": "messageSort",
        "send_event": "sendEvent",
        "receive_event": "receiveEvent",
        "interaction_operator": "interactionOperator",
        "body": "body",
        "represents": "represents",
        "diagram_id": "{{{xmi}}}id",
        "property_name": "name",
        "subject": "subject",
        "extender": "extender",
        "is_static": "isStatic",
        "is_abstract": "isAbstract",
        "is_ordered": "isOrdered",
        "is_unique": "isUnique",
        "is_read_only": "isReadOnly",
        "is_query": "isQuery",
        "is_derived": "isDerived",
        "is_derived_union": "isDerivedUnion",
        "value": "value",
    }

    PAPYRUS_EXTENDED_TAGS: dict[str, str] = {
        "elements": "elements",
        "element": "element",
        "model": "model",
        "package_properties": "packageproperties",
        "connectors": "connectors",
        "connector": "connector",
        "source": "source",
        "target": "target",
        "properties": "properties",
        "diagrams": "diagrams",
        "diagram": "diagram",
        "diagram_model": "model",
    }

    PAPYRUS_EXTENDED_ATTRIBUTES: dict[str, str] = {
        "idref": "{{{xmi}}}idref",
        "type": "{{{xmi}}}type",
        "name": "name",
        "package": "package",
        "connector_idref": "{{{xmi}}}idref",
        "connector_name": "name",
        "source_idref": "{{{xmi}}}idref",
        "target_idref": "{{{xmi}}}idref",
        "connector_type": "ea_type",
        "direction": "direction",
        "diagram_id": "{{{xmi}}}id",
        "diagram_package": "package",
        "property_name": "name",
        "property_type": "type",
        "element_name": "name",
        "subject": "subject",
    }

    PAPYRUS_DIAGRAMS_TYPES_MAPPING: dict[str, str] = {
        "PapyrusUMLClassDiagram": UmlDiagramType.CLASS,
        "PapyrusUMLSequenceDiagram": UmlDiagramType.SEQUENCE,
    }

    PAPYRUS_TYPE_ATTRIBUTE_MAPPING: dict[str, str] = {
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

    PAPYRUS_HREF_ATTRIBUTE_MAPPING: dict[str, str] = {
        "http://schema.omg.org/spec/UML/2.1/uml.xml#Integer": UmlPrimitiveTypeKindEnum.INTEGER,
    }

    # TODO: move to file with non-parsed constants /enums
    class PapyrusPackagedElementTypes(str, Enum):
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
        
