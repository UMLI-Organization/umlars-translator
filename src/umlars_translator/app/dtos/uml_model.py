import uuid
from typing import List, Optional, Union, Type, Dict, Any

from pydantic import BaseModel, ConfigDict, Field, field_serializer, model_validator

from umlars_translator.core.model.constants import (
    UmlVisibilityEnum,
    UmlParameterDirectionEnum,
    UmlMultiplicityEnum,
    UmlAssociationTypeEnum,
    UmlAssociationDirectionEnum,
    UmlInteractionOperatorEnum,
    UmlMessageSortEnum,
    UmlMessageKindEnum,
    UmlPrimitiveTypeKindEnum,
)


def serialize_field_to_id_reference(
    field: Optional[Union["UmlElement", "UmlIdReference"]]
) -> dict:
    if field is None:
        return None
    
    return (
        UmlIdReference.from_uml_element(field).model_dump()
        if isinstance(field, UmlElement)
        else field.model_dump()
    )


class UmlIdReference(BaseModel):
    idref: str

    @classmethod
    def from_uml_element(
        cls: Type["UmlIdReference"], element: "UmlElement"
    ) -> "UmlIdReference":
        return cls(idref=element.id)
    
    def __hash__(self) -> int:
        return hash(self.idref)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, UmlElement):
            return self.idref == other.id
        
        elif isinstance(other, UmlIdReference):
            return self.idref == other.idref
        
        return False


class UmlElement(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class UmlNamedElement(UmlElement):
    name: Optional[str] = None
    visibility: Optional[UmlVisibilityEnum] = UmlVisibilityEnum.PUBLIC


class UmlAttribute(UmlNamedElement):
    type: Optional[Union[
        "UmlPrimitiveType",
        "UmlClass",
        "UmlInterface",
        "UmlDataType",
        "UmlEnumeration",
        "UmlIdReference",
    ]] = None
    is_static: Optional[bool] = None
    is_ordered: Optional[bool] = None
    is_unique: Optional[bool] = None
    is_read_only: Optional[bool] = None
    is_query: Optional[bool] = None
    is_derived: Optional[bool] = None
    is_derived_union: Optional[bool] = None

    @field_serializer("type")
    def type_to_json(
        type: Optional[Union[
            "UmlPrimitiveType",
            "UmlClass",
            "UmlInterface",
            "UmlDataType",
            "UmlEnumeration",
            "UmlIdReference",
        ]]
    ) -> dict:
        return serialize_field_to_id_reference(type)


class UmlParameter(UmlNamedElement):
    type: Optional[Union[
        "UmlPrimitiveType",
        "UmlClass",
        "UmlInterface",
        "UmlDataType",
        "UmlEnumeration",
        "UmlIdReference",
    ]] = None
    direction: UmlParameterDirectionEnum = UmlParameterDirectionEnum.IN

    @field_serializer("type")
    def type_to_json(
        type: Optional[Union[
            "UmlPrimitiveType",
            "UmlClass",
            "UmlInterface",
            "UmlDataType",
            "UmlEnumeration",
            "UmlIdReference",
        ]]
    ) -> dict:
        return serialize_field_to_id_reference(type)


class UmlOperation(UmlNamedElement):
    parameters: List[UmlParameter] = Field(default_factory=list)
    return_type: Optional[Union[
        "UmlPrimitiveType",
        "UmlClass",
        "UmlInterface",
        "UmlDataType",
        "UmlEnumeration",
        "UmlIdReference",
    ]] = None
    is_static: Optional[bool] = None
    is_ordered: Optional[bool] = None
    is_unique: Optional[bool] = None
    is_query: Optional[bool] = None
    is_derived: Optional[bool] = None
    is_derived_union: Optional[bool] = None
    is_abstract: bool = False
    exceptions: List[str] = Field(default_factory=list)

    @field_serializer("return_type")
    def return_type_to_json(
        return_type: Optional[Union[
            "UmlPrimitiveType",
            "UmlClass",
            "UmlInterface",
            "UmlDataType",
            "UmlEnumeration",
            "UmlIdReference",
        ]]
    ) -> dict:
        return serialize_field_to_id_reference(return_type)


class UmlClassifier(UmlNamedElement):
    attributes: List[UmlAttribute] = Field(default_factory=list)
    operations: List[UmlOperation] = Field(default_factory=list)


class UmlClass(UmlClassifier):
    generalizations: List[Union["UmlGeneralization", "UmlIdReference"]] = Field(
        default_factory=list
    )
    interfaces: List[Union["UmlRealization", "UmlIdReference"]] = Field(
        default_factory=list
    )

    @field_serializer("generalizations")
    def generalizations_to_json(generalizations: List[UmlIdReference]) -> List[dict]:
        return [
            serialize_field_to_id_reference(super_class)
            for super_class in generalizations
        ]

    @field_serializer("interfaces")
    def interfaces_to_json(interfaces: List[UmlIdReference]) -> List[dict]:
        return [serialize_field_to_id_reference(interface) for interface in interfaces]


class UmlInterface(UmlClassifier):
    pass


class UmlDataType(UmlNamedElement):
    pass


class UmlEnumeration(UmlNamedElement):
    literals: List[str] = Field(default_factory=list)


class UmlPrimitiveType(UmlNamedElement):
    kind: UmlPrimitiveTypeKindEnum | str


class UmlAssociationEnd(UmlNamedElement):
    multiplicity: UmlMultiplicityEnum = UmlMultiplicityEnum.ONE
    element: Optional[Union[
        "UmlPrimitiveType",
        "UmlClass",
        "UmlInterface",
        "UmlDataType",
        "UmlEnumeration",
        "UmlAttribute",
        "UmlIdReference",
    ]] = None
    role: Optional[str] = None
    navigability: Optional[bool] = True

    @field_serializer("element")
    def element_to_json(
        element: Optional[Union[
            "UmlPrimitiveType",
            "UmlClass",
            "UmlInterface",
            "UmlDataType",
            "UmlEnumeration",
            "UmlAttribute",
            "UmlIdReference",
        ]]
    ) -> dict:
        return serialize_field_to_id_reference(element)


class UmlAssociation(UmlNamedElement):
    type: UmlAssociationTypeEnum = UmlAssociationTypeEnum.ASSOCIATION
    direction: UmlAssociationDirectionEnum = UmlAssociationDirectionEnum.BIDIRECTIONAL
    end1: Optional[Union["UmlAssociationEnd"]] = None
    end2: Optional[Union["UmlAssociationEnd"]] = None


class UmlDirectedAssociation(UmlNamedElement):
    type: UmlAssociationTypeEnum = UmlAssociationTypeEnum.ASSOCIATION
    direction: UmlAssociationDirectionEnum = UmlAssociationDirectionEnum.DIRECTED
    source: Optional[Union["UmlAssociationEnd", "UmlIdReference"]] = None
    target: Optional[Union["UmlAssociationEnd", "UmlIdReference"]] = None

    @field_serializer("source")
    def source_to_json(source: Optional[Union["UmlAssociationEnd", "UmlIdReference"]]) -> dict:
        return serialize_field_to_id_reference(source)

    @field_serializer("target")
    def target_to_json(target: Optional[Union["UmlAssociationEnd", "UmlIdReference"]]) -> dict:
        return serialize_field_to_id_reference(target)


class UmlAggregation(UmlDirectedAssociation):
    type: UmlAssociationTypeEnum = UmlAssociationTypeEnum.AGGREGATION


class UmlComposition(UmlDirectedAssociation):
    type: UmlAssociationTypeEnum = UmlAssociationTypeEnum.COMPOSITION


class UmlDependency(UmlElement):
    supplier: Optional[Union["UmlClass", "UmlInterface", "UmlIdReference"]] = None
    client: Optional[Union["UmlClass", "UmlInterface", "UmlIdReference"]] = None

    @field_serializer("supplier")
    def supplier_to_json(
        supplier: Optional[Union["UmlClass", "UmlInterface", "UmlIdReference"]]
    ) -> dict:
        return serialize_field_to_id_reference(supplier)

    @field_serializer("client")
    def client_to_json(
        client: Optional[Union["UmlClass", "UmlInterface", "UmlIdReference"]]
    ) -> dict:
        return serialize_field_to_id_reference(client)


class UmlRealization(UmlDependency):
    pass


class UmlGeneralization(UmlElement):
    specific: Optional[Union["UmlClass", "UmlInterface", "UmlIdReference"]] = None
    general: Optional[Union["UmlClass", "UmlInterface", "UmlIdReference"]] = None

    @field_serializer("specific")
    def specific_to_json(
        specific: Optional[Union["UmlClass", "UmlInterface", "UmlIdReference"]]
    ) -> dict:
        return serialize_field_to_id_reference(specific)

    @field_serializer("general")
    def general_to_json(
        general: Optional[Union["UmlClass", "UmlInterface", "UmlIdReference"]]
    ) -> dict:
        return serialize_field_to_id_reference(general)


class UmlOccurrenceSpecification(UmlElement):
    covered: Optional[Union["UmlLifeline", "UmlIdReference"]] = None

    @field_serializer("covered")
    def covered_to_json(
        covered: Optional[Union["UmlLifeline", "UmlIdReference"]]
    ) -> dict:
        return serialize_field_to_id_reference(covered)


class UmlInteractionUse(UmlNamedElement):
    interaction: Optional[Union["UmlInteraction", "UmlIdReference"]] = None
    covered: List[Union["UmlLifeline", "UmlIdReference"]] = Field(default_factory=list)

    @field_serializer("interaction")
    def interaction_to_json(
        interaction: Optional[Union["UmlInteraction", "UmlIdReference"]]
    ) -> dict:
        return serialize_field_to_id_reference(interaction)
    
    @field_serializer("covered")
    def covered_to_json(
        covered: List[Union["UmlLifeline", "UmlIdReference"]]
    ) -> List[dict]:
        return [serialize_field_to_id_reference(lifeline) for lifeline in covered]


class UmlCombinedFragment(UmlNamedElement):
    covered: List[Union["UmlLifeline", "UmlIdReference"]] = Field(default_factory=list)
    operands: List["UmlOperand"] = Field(default_factory=list)
    operator: UmlInteractionOperatorEnum

    @field_serializer("covered")
    def covered_to_json(
        covered: List[Union["UmlLifeline", "UmlIdReference"]]
    ) -> List[dict]:
        return [serialize_field_to_id_reference(lifeline) for lifeline in covered]
    


class UmlOperand(UmlElement):
    fragments: List[Union["UmlOccurrenceSpecification", "UmlCombinedFragment", "UmlInteractionUse"]] = Field(
        default_factory=list
    )
    guard: Optional[str] = None


class UmlLifeline(UmlNamedElement):
    represents: Optional[Union["UmlClass", "UmlInterface", "UmlIdReference"]] = None

    @field_serializer("represents")
    def represents_to_json(
        represents: Optional[Union["UmlClass", "UmlInterface", "UmlIdReference"]]
    ) -> dict:
        return serialize_field_to_id_reference(represents)


class UmlMessage(UmlNamedElement):
    send_event: Optional[Union["UmlOccurrenceSpecification", "UmlIdReference"]] = None
    receive_event: Optional[Union["UmlOccurrenceSpecification", "UmlIdReference"]] = None
    signature: Optional[Union["UmlOperation", "UmlIdReference"]] = None
    arguments: Optional[List[str]] = Field(default_factory=list)
    sort: UmlMessageSortEnum = UmlMessageSortEnum.SYNCH_CALL
    kind: UmlMessageKindEnum = UmlMessageKindEnum.COMPLETE
    
    @field_serializer("send_event")
    def send_event_to_json(
        send_event: Optional[Union["UmlOccurrenceSpecification", "UmlIdReference"]]
    ) -> dict:
        return serialize_field_to_id_reference(send_event)
    
    @field_serializer("receive_event")
    def receive_event_to_json(
        receive_event: Optional[Union["UmlOccurrenceSpecification", "UmlIdReference"]]
    ) -> dict:
        return serialize_field_to_id_reference(receive_event)
    
    @field_serializer("signature")
    def signature_to_json(
        signature: Optional[Union["UmlOperation", "UmlIdReference"]]
    ) -> dict:
        return serialize_field_to_id_reference(signature)


class UmlInteraction(UmlNamedElement):
    lifelines: List[UmlLifeline] = Field(default_factory=list)
    messages: List[UmlMessage] = Field(default_factory=list)
    fragments: List[Union["UmlOccurrenceSpecification", "UmlCombinedFragment", "UmlInteractionUse"]] = Field(
        default_factory=list
    )
    """
    Fragments are used to represent the different types of events that can occur in an interaction.
    Their order is important and they can be nested.
    """


class UmlPackage(UmlNamedElement):
    elements: Optional[Union["UmlModelElements", "UmlIdReference"]] = None

    @field_serializer("elements")
    def elements_to_json(
        elements: Optional[Union["UmlModelElements", "UmlIdReference"]]
    ) -> dict:
        return serialize_field_to_id_reference(elements)


class UmlModelElements(BaseModel):
    classes: List[UmlClass] = Field(default_factory=list)
    interfaces: List[UmlInterface] = Field(default_factory=list)
    data_types: List[UmlDataType] = Field(default_factory=list)
    enumerations: List[UmlEnumeration] = Field(default_factory=list)
    primitive_types: List[UmlPrimitiveType] = Field(default_factory=list)
    associations: List[Union["UmlAssociation", "UmlDirectedAssociation"]] = Field(default_factory=list)
    generalizations: List[UmlGeneralization] = Field(default_factory=list)
    dependencies: List[UmlDependency] = Field(default_factory=list)
    realizations: List[UmlRealization] = Field(default_factory=list)
    interactions: List[UmlInteraction] = Field(default_factory=list)
    packages: List["UmlPackage"] = Field(default_factory=list)

    @model_validator(mode="before")
    def check_unique_ids(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        id_map: Dict[str, UmlElement] = {}

        def collect_ids(element: UmlElement):
            if isinstance(element, UmlElement):
                if element.id in id_map:
                    if id_map[element.id] != element:
                        raise ValueError(f"Duplicate id found with different objects: {element.id}"
                                         f"\n{element}\n{id_map[element.id]}"
                                         )
                else:
                    id_map[element.id] = element

                # Recursively check nested objects like attributes, operations, etc.
                for field_name, field_value in element.__dict__.items():
                    if isinstance(field_value, list):
                        for item in field_value:
                            collect_ids(item)
                    elif isinstance(field_value, UmlElement):
                        collect_ids(field_value)

        # Iterate through each type of element in UmlModelElements
        if isinstance(values, dict):
            for element_list in values.values():
                if isinstance(element_list, list):
                    for element in element_list:
                        collect_ids(element)

        return values


class UmlDiagram(UmlElement):
    description: Optional[str] = None
    name: Optional[str] = None


class UmlSequenceDiagramElements(BaseModel):
    interactions: List[Union["UmlInteraction", "UmlIdReference"]] = Field(default_factory=list)

    @field_serializer("interactions")
    def interactions_to_json(interactions: List[Union["UmlInteraction", "UmlIdReference"]]) -> List[dict]:
        return [serialize_field_to_id_reference(interaction) for interaction in interactions]


class UmlSequenceDiagram(UmlDiagram):
    elements: UmlSequenceDiagramElements


class UmlClassDiagramElements(BaseModel):
    classes: List[Union["UmlClass", "UmlIdReference"]] = Field(default_factory=list)
    interfaces: List[Union["UmlInterface", "UmlIdReference"]] = Field(default_factory=list)
    data_types: List[Union["UmlDataType", "UmlIdReference"]] = Field(default_factory=list)
    enumerations: List[Union["UmlEnumeration", "UmlIdReference"]] = Field(default_factory=list)
    primitive_types: List[Union["UmlPrimitiveType", "UmlIdReference"]] = Field(default_factory=list)
    associations: List[Union["UmlAssociation", "UmlIdReference"]] = Field(default_factory=list)
    generalizations: List[Union["UmlGeneralization", "UmlIdReference"]] = Field(default_factory=list)
    dependencies: List[Union["UmlDependency", "UmlIdReference"]] = Field(default_factory=list)
    realizations: List[Union["UmlRealization", "UmlIdReference"]] = Field(default_factory=list)

    @field_serializer("classes")
    def classes_to_json(classes: List[Union["UmlClass", "UmlIdReference"]]) -> List[dict]:
        return [serialize_field_to_id_reference(class_) for class_ in classes]
                
    @field_serializer("interfaces")
    def interfaces_to_json(interfaces: List[Union["UmlInterface", "UmlIdReference"]]) -> List[dict]:
        return [serialize_field_to_id_reference(interface) for interface in interfaces]
                
    @field_serializer("data_types")
    def data_types_to_json(data_types: List[Union["UmlDataType", "UmlIdReference"]]) -> List[dict]:
        return [serialize_field_to_id_reference(dataType) for dataType in data_types]
                
    @field_serializer("enumerations")
    def enumerations_to_json(enumerations: List[Union["UmlEnumeration", "UmlIdReference"]]) -> List[dict]:
        return [serialize_field_to_id_reference(enumeration) for enumeration in enumerations]
                
    @field_serializer("primitive_types")
    def primitive_types_to_json(primitive_types: List[Union["UmlPrimitiveType", "UmlIdReference"]]) -> List[dict]:
        return [serialize_field_to_id_reference(primitiveType) for primitiveType in primitive_types]
                
    @field_serializer("associations")
    def associations_to_json(associations: List[Union["UmlAssociation", "UmlIdReference"]]) -> List[dict]:
        return [serialize_field_to_id_reference(association) for association in associations]
                
    @field_serializer("generalizations")
    def generalizations_to_json(generalizations: List[Union["UmlGeneralization", "UmlIdReference"]]) -> List[dict]:
        return [serialize_field_to_id_reference(generalization) for generalization in generalizations]
                
    @field_serializer("dependencies")
    def dependencies_to_json(dependencies: List[Union["UmlDependency", "UmlIdReference"]]) -> List[dict]:
        return [serialize_field_to_id_reference(dependency) for dependency in dependencies]
                
    @field_serializer("realizations")
    def realizations_to_json(realizations: List[Union["UmlRealization", "UmlIdReference"]]) -> List[dict]:
        return [serialize_field_to_id_reference(realization) for realization in realizations]


class UmlClassDiagram(UmlDiagram):
    elements: UmlClassDiagramElements


class UmlDiagrams(BaseModel):
    class_diagrams: List[Union[UmlClassDiagram, UmlIdReference]] = Field(default_factory=list)
    sequence_diagrams: List[Union[UmlSequenceDiagram, UmlIdReference]] = Field(default_factory=list)


class UmlModel(UmlNamedElement):
    elements: UmlModelElements
    diagrams: UmlDiagrams
    metadata: dict = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_mongo(cls, mongo_dict: dict) -> "UmlModel":
        """Convertion is required for _id key into "id". """
        if not mongo_dict:
            return mongo_dict
        id = mongo_dict.pop('_id', None)
        return cls(**dict(mongo_dict, id=str(id)))