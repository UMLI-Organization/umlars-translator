from typing import Iterator, Any

from src.umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline import (
    ModelProcessingPipe,
    DataBatch,
)
from src.umlars_translator.core.deserialization.abstract.json.json_pipeline import (
    JSONModelProcessingPipe,
    JSONAttributeCondition,
    AliasToJSONKey
)
from src.umlars_translator.core.deserialization.formats.staruml_mdj.staruml_constants import (
    StarumlMDJConfig
)
from src.umlars_translator.core.deserialization.exceptions import InvalidFormatException, UnableToMapError


class StarumlMDJModelProcessingPipe(JSONModelProcessingPipe):
    pass


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
                visibility=StarumlMDJConfig.KEYS["visibility"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes
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
                type=StarumlMDJConfig.KEYS["type"],
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

        self.model_builder.construct_uml_attribute(**aliases_to_values, classifier_id=data_batch.parent_context.get("parent_id"))

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

        self.model_builder.construct_uml_operation(**aliases_to_values, classifier_id=data_batch.parent_context.get("parent_id"))

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
                name=StarumlMDJConfig.KEYS["name"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes
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

        self.model_builder.construct_uml_association_end(
            **aliases_to_values, association_id=data_batch.parent_context.get("parent_id")
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
        
        self.model_builder.construct_uml_interface_realization(**aliases_to_values)
        
        yield from self._create_data_batches([])


class UmlOperationParameterPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLParameter"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                id=StarumlMDJConfig.ATTRIBUTES["id"],
                name=StarumlMDJConfig.ATTRIBUTES["name"],
            )

            optional_attributes = AliasToJSONKey.from_kwargs(
                type=StarumlMDJConfig.ATTRIBUTES["type"],
                direction=StarumlMDJConfig.ATTRIBUTES["direction"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        # Handling the 'type' attribute if it references another element
        try:
            self._map_value_from_key(
                aliases_to_values, "type", StarumlMDJConfig.ELEMENT_REFERENCE_MAPPING
            )
        except UnableToMapError:
            type_attr_value = aliases_to_values.pop("type", None)
            if type_attr_value is not None:
                self._logger.debug(
                    f"Assuming type attribute value: {type_attr_value} is an ID reference."
                )
                aliases_to_values["type_id"] = type_attr_value

        self.model_builder.construct_uml_operation_parameter(
            **aliases_to_values, operation_id=data_batch.parent_context["parent_id"]
        )
        
        yield from self._create_data_batches(data)

