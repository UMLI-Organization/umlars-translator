from typing import Iterator

from umlars_translator.core.deserialization.abstract.json.json_pipeline import (
    JSONFormatDetectionPipe,
    DataBatch,
    JSONAttributeCondition,
)
from umlars_translator.core.deserialization.exceptions import InvalidFormatException


class StarumlMDJFormatDetectionPipe(JSONFormatDetectionPipe):
    ...


class StarumlMDJDetectionPipe(StarumlMDJFormatDetectionPipe):
    ATTRIBUTE_CONDITIONS = [
        JSONAttributeCondition(attribute_name="_type", expected_value="Project"),
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        if not isinstance(data, dict):
            raise InvalidFormatException(f"Expected dict, got {type(data)}")
        
        # Iteration over the children of the root element
        yield from self._create_data_batches(data_batch.data.items())
