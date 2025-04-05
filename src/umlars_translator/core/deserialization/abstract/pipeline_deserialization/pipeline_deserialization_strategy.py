from abc import abstractmethod
from typing import Optional, Any

from umlars_translator.core.deserialization.abstract.base.deserialization_strategy import (
    DeserializationStrategy,
)
from umlars_translator.core.deserialization.data_source import DataSource
from umlars_translator.core.model.abstract.uml_model import IUmlModel
from umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline import (
    ModelProcessingPipe,
    FormatDetectionPipe,
)
from umlars_translator.core.deserialization.exceptions import InvalidFormatException


class PipelineDeserializationStrategy(DeserializationStrategy):
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

    @property
    def pipe(self) -> ModelProcessingPipe:
        if self._pipe is None:
            # TODO: possible improvement - based on supposition format_detection_pipe is similar to the main pipe, it could be used as a base for the main pipe
            # However, it would require some additional logic to handle the differences between the two implemented in the subclasses of this deserilization strategy.
            # if self._format_detection_pipe is not None:
            #     self._pipe = self._build_processing_pipe(based_on_format_detection_pipe=True)
            # else:
            #     self._pipe = self._build_processing_pipe()
            self._create_new_processing_pipe()
        return self._pipe

    @property
    def format_detection_pipe(self) -> FormatDetectionPipe:
        if self._format_detection_pipe is None:
            self._create_new_format_detection_pipe()
        return self._format_detection_pipe

    def synchronize_pipe(self, pipe: ModelProcessingPipe) -> None:
        self.set_pipe_builder(pipe)
        self.set_pipe_config(pipe)

    def set_pipe_config(self, pipe: ModelProcessingPipe) -> None:
        pipe.set_config(self.config)

    def set_pipe_builder(self, pipe: ModelProcessingPipe) -> None:
        pipe.set_model_builder(self.model_builder)

    def clear(self) -> None:
        self._pipe = None
        self._format_detection_pipe = None
        self._parsed_data = None
        self._model_builder.clear()

    def _create_new_processing_pipe(self) -> None:
        self._pipe = self._build_processing_pipe()
        self.synchronize_pipe(self.pipe)

    def _create_new_format_detection_pipe(self) -> None:
        self._format_detection_pipe = self._build_format_detection_pipe()
        self.synchronize_pipe(self.format_detection_pipe)

    def _can_deserialize_format_data(
        self, format_data: DataSource, cache_parsed_data: bool = True
    ) -> bool:
        """
        Helper method used to check if the format data is valid for deserialization.
        Using format detection pipe allows for kind of lazy instantiation of the main pipe, in case it is not needed.
        """
        try:
            parsed_data = self._parse_format_data(format_data)
        except InvalidFormatException as ex:
            message = f"Unable to parse format data: {ex}"
            self._logger.info(message)
            return False

        if cache_parsed_data:
            self._parsed_data = parsed_data
        return self.format_detection_pipe.is_supported_format(parsed_data)

    def _retrieve_model(
        self, data_source: DataSource, clear_afterwards: bool = True
    ) -> IUmlModel:
        self._parsed_data = (
            self._parse_format_data(data_source)
            if self._parsed_data is None
            else self._parsed_data
        )
        retrieved_model = self._process_data(self._parsed_data)
        
        if clear_afterwards:
            self.clear()

        return retrieved_model

    def _parse_format_data(self, data_source: DataSource) -> Any:
        """
        Method used to retrieve the intermediate data representation used in further processing.
        It may consist of some pre-parsed objects specific for that format, created using existing library.

        This base version retrieves data as a string and should be overloaded, if better approach is available.
        """
        return data_source.retrieved_data

    def _process_data(self, data: Any) -> IUmlModel:
        self.pipe.process(data)
        return self.pipe.get_model()

    @abstractmethod
    def _build_processing_pipe(self) -> ModelProcessingPipe:
        ...

    @abstractmethod
    def _build_format_detection_pipe(self) -> FormatDetectionPipe:
        ...
