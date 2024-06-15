from umlars_translator.core.model.constants import DiagramType


NAMESPACES: dict[str, str] = {
    "UML_2_1": "{http://schema.omg.org/spec/UML/2.1}",
    "XMI_2_1": "{http://schema.omg.org/spec/XMI/2.1}",
}

TAGS: dict[str, str] = {
    "root": f"{NAMESPACES['XMI_2_1']}XMI",
    "documentation": f"{NAMESPACES['XMI_2_1']}Documentation",
    "model": f"{NAMESPACES['UML_2_1']}Model",
    "owned_end": "ownedEnd",
    "end_type": "type",
    "owned_attribute": "ownedAttribute",
    "sequence_behavior": "ownedBehavior",
    "attribute_type": "type",
    "operation": "ownedOperation",
    "operation_parameter": "ownedParameter",
    "parameter_type": "type",
    "property_type": "type",
    "covered": "covered",
    "operand": "operand",
    "guard": "guard",
    "specification": "specification",
    "extension": f"{NAMESPACES['XMI_2_1']}Extension",
    "diagrams": "diagrams",
    "diagram": "diagram",
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
    "id": f"{NAMESPACES['XMI_2_1']}id",
    "type": f"{NAMESPACES['XMI_2_1']}type",
    "xmi_version": f"{NAMESPACES['XMI_2_1']}version",
    "exporter": "exporter",
    "exporterVersion": "exporterVersion",
    "exporterID": "exporterID",
    "name": "name",
    "idref": f"{NAMESPACES['XMI_2_1']}idref",
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
    "diagram_id": f"{NAMESPACES['XMI_2_1']}id",
    "property_name": "name",
    "subject": "subject",
    "extender": "extender",
}


EA_EXTENDED_TAGS: dict[str, str] = {
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

EA_EXTENDED_ATTRIBUTES: dict[str, str] = {
    "idref": f"{NAMESPACES['XMI_2_1']}idref",
    "type": f"{NAMESPACES['XMI_2_1']}type",
    "name": "name",
    "package": "package",
    "connector_idref": f"{NAMESPACES['XMI_2_1']}idref",
    "connector_name": "name",
    "source_idref": f"{NAMESPACES['XMI_2_1']}idref",
    "target_idref": f"{NAMESPACES['XMI_2_1']}idref",
    "connector_type": "ea_type",
    "direction": "direction",
    "diagram_id": f"{NAMESPACES['XMI_2_1']}id",
    "diagram_package": "package",
    "property_name": "name",
    "subject": "subject",
}


EA_DIAGRAMS_TYPES: dict[str, str] = {
    "Logical": DiagramType.CLASS,
    "Sequence": DiagramType.SEQUENCE,
}