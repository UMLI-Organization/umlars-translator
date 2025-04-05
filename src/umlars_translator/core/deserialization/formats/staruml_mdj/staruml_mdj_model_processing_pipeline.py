from typing import Iterator, Any, Optional

from umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline import (
    ModelProcessingPipe,
    DataBatch,
)
from umlars_translator.core.deserialization.abstract.json.json_pipeline import (
    JSONModelProcessingPipe,
    JSONAttributeCondition,
    AliasToJSONKey
)
from umlars_translator.core.deserialization.formats.staruml_mdj.staruml_constants import (
    StarumlMDJConfig
)
from umlars_translator.core.deserialization.exceptions import InvalidFormatException, UnableToMapError
from umlars_translator.core.model.constants import UmlPrimitiveTypeKindEnum, UmlMessageSortEnum, UmlInteractionOperatorEnum


class StarumlMDJModelProcessingPipe(JSONModelProcessingPipe):
    def _flatten_reference(self, data: dict, key: str, new_key: Optional[str] = None, reference_key: str = "$ref", remove_key: bool = False) -> dict:
        if key not in data:
            return data

        reference = data[key] if not remove_key else data.pop(key)

        if reference_key not in reference:
            return data

        new_key = new_key or key

        try:
            data[new_key] = reference[reference_key]
        except KeyError as ex:
            raise UnableToMapError(f"Expected dict, got {type(reference)}") from ex

        return data


class RootPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="Project"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        if not isinstance(data, dict):
            raise InvalidFormatException(f"Expected dict, got {type(data)}")

        yield from self._create_data_batches(data.get(StarumlMDJConfig.KEYS["owned_elements"], []))


class UmlModelPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLModel"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                name=StarumlMDJConfig.KEYS["name"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes
        )

        self.model_builder.construct_uml_model(**aliases_to_values)

        yield from self._create_data_batches(data.get(StarumlMDJConfig.KEYS["owned_elements"], []))


class UmlClassPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLClass"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                name=StarumlMDJConfig.KEYS["name"],
            )
            optional_attributes = AliasToJSONKey.from_kwargs(
                visibility=StarumlMDJConfig.KEYS["visibility"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self.model_builder.construct_uml_class(**aliases_to_values)

        yield from self._create_data_batches(
            data.get(StarumlMDJConfig.KEYS["owned_elements"], []) +
            data.get(StarumlMDJConfig.KEYS["attributes"], []) +
            data.get(StarumlMDJConfig.KEYS["operations"], [])
        )


class UmlInterfacePipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLInterface"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                name=StarumlMDJConfig.KEYS["name"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes
        )

        self.model_builder.construct_uml_interface(**aliases_to_values)

        yield from self._create_data_batches(data.get(StarumlMDJConfig.KEYS["operations"], []))


class UmlDataTypePipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLDataType"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                name=StarumlMDJConfig.KEYS["name"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes
        )

        self.model_builder.construct_uml_data_type(**aliases_to_values)

        yield from self._create_data_batches([])


class UmlEnumerationPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLEnumeration"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                name=StarumlMDJConfig.KEYS["name"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes
        )

        self.model_builder.construct_uml_enumeration(**aliases_to_values)

        yield from self._create_data_batches([])


class UmlAttributePipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLAttribute"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                name=StarumlMDJConfig.KEYS["name"],
                type=StarumlMDJConfig.KEYS["type_ref"],
                classifier_id=StarumlMDJConfig.KEYS["parent_id"],
            )
            optional_attributes = AliasToJSONKey.from_kwargs(
                visibility=StarumlMDJConfig.KEYS["visibility"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self._flatten_reference(aliases_to_values, "type", "type_id", remove_key=True)
        self._flatten_reference(aliases_to_values, "classifier_id", remove_key=True)
        self.model_builder.construct_uml_attribute(**aliases_to_values)

        yield from self._create_data_batches([])


class UmlOperationPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLOperation"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                name=StarumlMDJConfig.KEYS["name"],
                classifier_id=StarumlMDJConfig.KEYS["parent_id"],
            )
            optional_attributes = AliasToJSONKey.from_kwargs(
                visibility=StarumlMDJConfig.KEYS["visibility"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self._flatten_reference(aliases_to_values, "classifier_id", remove_key=True)
        self.model_builder.construct_uml_operation(**aliases_to_values)

        yield from self._create_data_batches(data.get(StarumlMDJConfig.KEYS["parameters"], []))


class UmlAssociationPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLAssociation"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
            )
            optional_attributes = AliasToJSONKey.from_kwargs(
                name=StarumlMDJConfig.KEYS["name"],
                visibility=StarumlMDJConfig.KEYS["visibility"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self.model_builder.construct_uml_association(**aliases_to_values)

        yield from self._create_data_batches(
            [data.get(StarumlMDJConfig.KEYS["end1"], {}), data.get(StarumlMDJConfig.KEYS["end2"], {})]
        )


class UmlAssociationEndPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLAssociationEnd"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                name=StarumlMDJConfig.KEYS["name"],
                reference=StarumlMDJConfig.KEYS["reference"],
                association_id=StarumlMDJConfig.KEYS["parent_id"],
            )
            optional_attributes = AliasToJSONKey.from_kwargs(
                multiplicity=StarumlMDJConfig.KEYS["multiplicity"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self._map_value_from_key(aliases_to_values, "multiplicity", StarumlMDJConfig.MULTIPLICITY_MAPPING, raise_when_missing=False)

        self._flatten_reference(aliases_to_values, "association_id", remove_key=True)
        self._flatten_reference(aliases_to_values, "reference", "type_id", remove_key=True)

        self.model_builder.construct_uml_association_end(
            **aliases_to_values
        )

        yield from self._create_data_batches([])


class UmlGeneralizationPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLGeneralization"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        
        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                source=StarumlMDJConfig.KEYS["source"],
                target=StarumlMDJConfig.KEYS["target"],
            )
        except KeyError as ex:
            raise ValueError(f"Configuration of the data format was invalid. Error: {str(ex)}")
        
        aliases_to_values = self._get_attributes_values_for_aliases(data, mandatory_attributes)
        
        self._flatten_reference(aliases_to_values, "source", "specific_id", remove_key=True)
        self._flatten_reference(aliases_to_values, "target", "general_id", remove_key=True)
        self.model_builder.construct_uml_generalization(**aliases_to_values)
        
        yield from self._create_data_batches([])


class UmlInterfaceRealizationPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLInterfaceRealization"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        
        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                source=StarumlMDJConfig.KEYS["source"],
                target=StarumlMDJConfig.KEYS["target"],
            )
        except KeyError as ex:
            raise ValueError(f"Configuration of the data format was invalid. Error: {str(ex)}")
        
        aliases_to_values = self._get_attributes_values_for_aliases(data, mandatory_attributes)
        
        self._flatten_reference(aliases_to_values, "source", "client_id", remove_key=True)
        self._flatten_reference(aliases_to_values, "target", "supplier_id", remove_key=True)
        self.model_builder.construct_uml_realization(**aliases_to_values)
        
        yield from self._create_data_batches([])


class UmlOperationParameterPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLParameter"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                operation_id=StarumlMDJConfig.KEYS["parent_id"],
            )

            optional_attributes = AliasToJSONKey.from_kwargs(
                name=StarumlMDJConfig.KEYS["name"],
                type=StarumlMDJConfig.KEYS["type_ref"],
                direction=StarumlMDJConfig.KEYS["direction"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self._flatten_reference(aliases_to_values, "type", "type_id", remove_key=True)
        self._flatten_reference(aliases_to_values, "operation_id", remove_key=True)
        self.model_builder.construct_uml_parameter(
            **aliases_to_values
        )
        
        yield from self._create_data_batches(data)


class UmlPrimitiveTypePipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLPrimitiveType"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                name=StarumlMDJConfig.KEYS["name"],
                kind=StarumlMDJConfig.KEYS["name"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes
        )

        try:
            self._map_value_from_key(aliases_to_values, "kind", StarumlMDJConfig.PRIMITIVE_TYPE_MAPPING, raise_when_missing=True)
        except UnableToMapError as ex:
            self._logger.error(f"Unable to map primitive type: {ex}. Using default value: {UmlPrimitiveTypeKindEnum.ANY}")
            aliases_to_values["kind"] = UmlPrimitiveTypeKindEnum.ANY

        self.model_builder.construct_uml_primitive_type(**aliases_to_values)

        yield from self._create_data_batches([])


class UmlClassDiagramPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLClassDiagram"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                name=StarumlMDJConfig.KEYS["name"],
            )
            optional_attributes = AliasToJSONKey.from_kwargs(
                visibility=StarumlMDJConfig.KEYS["visibility"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )
        
        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self.model_builder.construct_class_diagram(**aliases_to_values)

        yield from self._create_data_batches(data.get(StarumlMDJConfig.KEYS["owned_views"], []), parent_context={"diagram_id": aliases_to_values["id"]})


class UmlAnyViewPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition.from_regex(attribute_name="_type", expected_value="UML.*View"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                model=StarumlMDJConfig.KEYS["model"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )
        
        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes
        )

        self._flatten_reference(aliases_to_values, "model", "element_id", remove_key=True)
        aliases_to_values["diagram_id"] = data_batch.parent_context["diagram_id"]

        self.model_builder.bind_element_to_diagram(**aliases_to_values)

        yield from self._create_data_batches(data.get(StarumlMDJConfig.KEYS["owned_views"], []), parent_context={"diagram_id": aliases_to_values["diagram_id"]})


class UmlCollaborationPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLCollaboration"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        yield from self._create_data_batches(data.get(StarumlMDJConfig.KEYS["owned_elements"], []))


class UmlInteractionPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLInteraction"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                name=StarumlMDJConfig.KEYS["name"],
            )
            optional_attributes = AliasToJSONKey.from_kwargs(
                visibility=StarumlMDJConfig.KEYS["visibility"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )
        
        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self.model_builder.construct_uml_interaction(**aliases_to_values)

        yield from self._create_data_batches(data.get(StarumlMDJConfig.KEYS["owned_elements"], []) +
                                             data.get(StarumlMDJConfig.KEYS["messages"], []) + 
                                             data.get(StarumlMDJConfig.KEYS["participants"], []) +
                                             data.get(StarumlMDJConfig.KEYS["fragments"], []),
                                             parent_context={"interaction_id": aliases_to_values["id"]})

    
class UmlSequenceDiagramPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLSequenceDiagram"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                name=StarumlMDJConfig.KEYS["name"],
            )
            optional_attributes = AliasToJSONKey.from_kwargs(
                visibility=StarumlMDJConfig.KEYS["visibility"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )
        
        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self.model_builder.construct_sequence_diagram(**aliases_to_values)
        self.model_builder.bind_element_to_diagram(element_id=data_batch.parent_context["interaction_id"], diagram_id=aliases_to_values["id"])

        yield from self._create_data_batches(data.get(StarumlMDJConfig.KEYS["owned_views"], []), parent_context={"diagram_id": aliases_to_values["id"]})


class UmlMessagePipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLMessage"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                name=StarumlMDJConfig.KEYS["name"],
                source=StarumlMDJConfig.KEYS["source"],
                target=StarumlMDJConfig.KEYS["target"],
                interaction_id=StarumlMDJConfig.KEYS["parent_id"],
            )
            optional_attributes = AliasToJSONKey.from_kwargs(
                visibility=StarumlMDJConfig.KEYS["visibility"],
                message_sort=StarumlMDJConfig.KEYS["message_sort"],
                signature=StarumlMDJConfig.KEYS["signature"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )
        
        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self._flatten_reference(aliases_to_values, "source", "source_lifeline_id", remove_key=True)
        self._flatten_reference(aliases_to_values, "target", "target_lifeline_id", remove_key=True)
        self._flatten_reference(aliases_to_values, "interaction_id", remove_key=True)
        self._flatten_reference(aliases_to_values, "signature", "signature_id", remove_key=True)

        try:
            self._map_value_from_key(aliases_to_values, "message_sort", StarumlMDJConfig.MESSAGE_SORT_MAPPING, raise_when_missing=True)
        except UnableToMapError as ex:
            self._logger.error(f"Unable to map message sort: {ex}. Using default value: {UmlMessageSortEnum.SYNCH_CALL}")
            aliases_to_values["message_sort"] = UmlMessageSortEnum.SYNCH_CALL

        self.model_builder.construct_uml_message(**aliases_to_values, create_new_occurences=True)

        yield from self._create_data_batches([])


class UmlLifelinePipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLLifeline"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                name=StarumlMDJConfig.KEYS["name"],
                interaction_id=StarumlMDJConfig.KEYS["parent_id"],
            )
            optional_attributes = AliasToJSONKey.from_kwargs(
                visibility=StarumlMDJConfig.KEYS["visibility"],
                represents_id=StarumlMDJConfig.KEYS["represent"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )
        
        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self._flatten_reference(aliases_to_values, "interaction_id", remove_key=True)
        self._flatten_reference(aliases_to_values, "represents_id", remove_key=True)

        self.model_builder.construct_uml_lifeline(**aliases_to_values)

        yield from self._create_data_batches(data.get(StarumlMDJConfig.KEYS["fragments"], []))

    
class UmlCombinedFragmentPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLCombinedFragment"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                operator=StarumlMDJConfig.KEYS["operator"],
                interaction_id=StarumlMDJConfig.KEYS["parent_id"],
            )
            optional_attributes = AliasToJSONKey.from_kwargs(
                name=StarumlMDJConfig.KEYS["name"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )
        
        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self._flatten_reference(aliases_to_values, "interaction_id", remove_key=True)

        try:
            self._map_value_from_key(aliases_to_values, "operator", StarumlMDJConfig.COMBINED_FRAGMENT_OPERATOR_MAPPING, raise_when_missing=True)
        except UnableToMapError as ex:
            self._logger.error(f"Unable to map combined fragment operator: {ex}. Using default value: {UmlInteractionOperatorEnum.ALT}")
            aliases_to_values["operator"] = UmlInteractionOperatorEnum.ALT

        self.model_builder.construct_uml_combined_fragment(**aliases_to_values)

        yield from self._create_data_batches(data.get(StarumlMDJConfig.KEYS["operands"], []))


class UmlInteractionOperandPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLInteractionOperand"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                guard=StarumlMDJConfig.KEYS["guard"],
                combined_fragment_id=StarumlMDJConfig.KEYS["parent_id"],
            )
            optional_attributes = AliasToJSONKey.from_kwargs(
                name=StarumlMDJConfig.KEYS["name"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )
        
        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self._flatten_reference(aliases_to_values, "combined_fragment_id", remove_key=True)

        self.model_builder.construct_uml_operand(**aliases_to_values)

        yield from self._create_data_batches(data.get(StarumlMDJConfig.KEYS["fragments"], []))


class UmlInteractionUsePipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLInteractionUse"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.KEYS["id"],
                referred_interaction_id=StarumlMDJConfig.KEYS["refers_to"],
                parent_interaction_id=StarumlMDJConfig.KEYS["parent_id"],
            )
            optional_attributes = AliasToJSONKey.from_kwargs(
                name=StarumlMDJConfig.KEYS["name"],
                visibility=StarumlMDJConfig.KEYS["visibility"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )
        
        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self._flatten_reference(aliases_to_values, "referred_interaction_id", remove_key=True)
        self._flatten_reference(aliases_to_values, "parent_interaction_id", remove_key=True)

        self.model_builder.construct_uml_interaction_use(**aliases_to_values)

        yield from self._create_data_batches([])