from typing import Iterator, Any

from src.umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline import (
    ModelProcessingPipe,
    FormatDetectionPipe,
    DataBatch,
)
from src.umlars_translator.core.deserialization.exceptions import UnableToMapError
from src.umlars_translator.core.model.constants import UmlDiagramType
from src.umlars_translator.core.deserialization.abstract.json.json_pipeline import (
    JSONModelProcessingPipe,
    JSONAttributeCondition,
    AliasToJSONKey
)
from src.umlars_translator.core.deserialization.formats.staruml_mdj.staruml_constants import (
    StarumlMDJConfig
)
from src.umlars_translator.core.deserialization.exceptions import InvalidFormatException


class StarumlMDJModelProcessingPipe(JSONModelProcessingPipe):
    ...


class RootPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="Project"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        if not isinstance(data, dict):
            raise InvalidFormatException(f"Expected dict, got {type(data)}")

        # Iteration over the children of the root element
        yield from self._create_data_batches(data_batch.data[StarumlMDJConfig.KEYS["owned_elements"]])


class UmlModelPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLModel"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                name=self.config.ATTRIBUTES["id"],
            )
            optional_attributes = AliasToJSONKey.from_kwargs(
                xmi_version=self.config.ATTRIBUTES["name"]
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self.model_builder.construct_uml_model(**aliases_to_values)

        yield from self._create_data_batches(data[StarumlMDJConfig.KEYS["owned_elements"]])


class UmlClassPipe(StarumlMDJModelProcessingPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="UMLClass"), 
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToJSONKey.from_kwargs(
                name=self.config.ATTRIBUTES["name"],
                visibility=self.config.ATTRIBUTES["visibility"],
            )
            optional_attributes = AliasToJSONKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"],
                type=self.config.ATTRIBUTES["type"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )
        
        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self.model_builder.construct_uml_class(**aliases_to_values)

        yield from self._create_data_batches(data[StarumlMDJConfig.KEYS["owned_elements"]] + data[StarumlMDJConfig.KEYS["owned_attributes"]])

