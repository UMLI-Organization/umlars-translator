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


# class ModelPipe(StarumlMDJModelProcessingPipe):
#     ATTRIBUTE_CONDITIONS = [
#         JSONAttributeCondition(attribute_name="_type", expected_value="UMLModel"),
#     ]

#     def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
#         data = data_batch.data
#         if not isinstance(data, dict):
#             raise InvalidFormatException(f"Expected dict, got {type(data)}")

#         # Iteration over the children of the root element
#         yield from self._create_data_batches(data_batch.data[KEYS["owned_elements"]])