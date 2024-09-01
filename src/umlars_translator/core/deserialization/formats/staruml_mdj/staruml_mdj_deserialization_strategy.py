from abc import abstractmethod
from typing import Optional, Any
import json

from src.umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline_deserialization_strategy import (
    PipelineDeserializationStrategy,
)
from src.umlars_translator.core.deserialization.data_source import DataSource
from src.umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline import (
    ModelProcessingPipe,
    FormatDetectionPipe,
)
from src.umlars_translator.core.deserialization.exceptions import InvalidFormatException
from src.umlars_translator.core.deserialization.formats.staruml_mdj.staruml_mdj_format_detection_pipeline import (
    StarumlMDJDetectionPipe
)
from src.umlars_translator.core.deserialization.formats.staruml_mdj.staruml_mdj_model_processing_pipeline import (
    RootPipe
)
from src.umlars_translator.core.deserialization.factory import (
    register_deserialization_strategy,
)
from src.umlars_translator.config import SupportedFormat
from src.umlars_translator.core.deserialization.formats.staruml_mdj.staruml_constants import (
    StarumlMDJConfig,
)


class JSONDeserializationStrategy(PipelineDeserializationStrategy):
    def __init__(
        self,
        pipe: Optional[ModelProcessingPipe] = None,
        format_detection_pipe: Optional[ModelProcessingPipe] = None,
        **kwargs,
    ) -> None:
        self._pipe = pipe
        self._format_detection_pipe = format_detection_pipe
        self._parsed_data = None
        super().__init__(**kwargs)

    def _parse_format_data(self, data_source: DataSource) -> Any:
        try:
            return json.loads(data_source.retrieved_data)
        except json.JSONDecodeError as ex:
            error_message = f"Error parsing JSON data from {data_source}: {ex}"
            self._logger.error(error_message)
            raise InvalidFormatException(error_message)


@register_deserialization_strategy
class StarumlMDJDeserializationStrategy(JSONDeserializationStrategy):
    SUPPORTED_FORMAT_NAME = SupportedFormat.MDJ_STARTUML
    CONFIG_NAMESPACE_CLASS = StarumlMDJConfig

    def _build_processing_pipe(self) -> ModelProcessingPipe:
        root_pipe = RootPipe()
        return root_pipe

    def _build_format_detection_pipe(self) -> FormatDetectionPipe:
        return StarumlMDJDetectionPipe()
