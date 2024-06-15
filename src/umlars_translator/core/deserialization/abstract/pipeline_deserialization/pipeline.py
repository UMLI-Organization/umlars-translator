from abc import ABC, abstractmethod
from typing import Optional, Callable, NamedTuple, Any, Iterator
from logging import Logger

from kink import inject

from umlars_translator.core.deserialization.abstract.base.deserialization_strategy import (
    DeserializationStrategy,
)
from umlars_translator.core.deserialization.data_source import DataSource
from umlars_translator.core.deserialization.exceptions import (
    UnsupportedFormatException,
    InvalidFormatException,
)
from umlars_translator.core.model.uml_model import UMLModel
from umlars_translator.core.model.uml_model_builder import UmlModelBuilder


@inject
class ModelProcessingPipe(ABC):
    def __init__(
        self,
        successors: Optional[Iterator["ModelProcessingPipe"]] = None,
        predecessor: Optional["ModelProcessingPipe"] = None,
        model_builder: Optional[UmlModelBuilder] = None,
        logger: Optional[Logger] = None,
    ) -> None:
        self._successors = successors if successors is not None else []
        self._predecessor = predecessor
        self._model_builder = model_builder or UmlModelBuilder()
        self._logger = logger.getChild(self.__class__.__name__)

    @property
    def model_builder(self) -> UmlModelBuilder:
        return self._model_builder

    @model_builder.setter
    def model_builder(self, new_model_builder: UmlModelBuilder) -> None:
        self._model_builder = new_model_builder

    @property
    def predecessor(self) -> Optional["ModelProcessingPipe"]:
        return self._predecessor

    @predecessor.setter
    def predecessor(self, value: Optional["ModelProcessingPipe"]) -> None:
        self._predecessor = value

    def add_next(
        self, pipe: "ModelProcessingPipe", share_builder: bool = True
    ) -> "ModelProcessingPipe":
        self._successors.append(pipe)
        if share_builder:
            pipe.model_builder = self.model_builder

        pipe.add_predecessor(self)
        return pipe

    def add_predecessor(self, pipe: "ModelProcessingPipe") -> "ModelProcessingPipe":
        if self not in pipe._successors:
            pipe.add_next(self)
        self._predecessor = pipe

    def process_if_possible(self, data) -> None:
        if self.can_run_for(data):
            self.process(data)

    def process(self, data) -> None:
        batches_of_data_processed_by_parent = self._process(data)

        for successor in self._successors:
            for data_processed_by_parent in batches_of_data_processed_by_parent:
                successor.process_if_possible(data_processed_by_parent)

    def get_model(self) -> UMLModel:
        return self.model_builder.build()

    def can_run_for(self, data) -> bool:
        return self._can_process(data)

    @abstractmethod
    def _process(self, data) -> Iterator[Any]:
        """
        Processes the accepted data in a way defined by the subclass. Returns data splitted into parts to be processed by successor pipes.
        Throws InvalidFormatException if the data is not valid for the pipe. It can be avoided by checking the data before processing using can_run_for method.
        """
        ...

    @abstractmethod
    def _can_process(self, data) -> bool:
        """
        Method overrided in each subclass. Defines, whether the received data can be parsed by default pipe of such type.
        """


class FormatDetectionPipe(ModelProcessingPipe):
    def is_supported_format(self, data) -> bool:
        if not self.can_run_for(data):
            return False

        try:
            self.process(data)
            return True
        except UnsupportedFormatException as ex:
            self._logger.debug(f"Format is not supported: {ex}")
            return False

    @abstractmethod
    def _process(self, data) -> Iterator[Any]:
        """
        Throws UnsupportedFormatException if the format indicators are invalid in regards to the represented format.
        """
        ...
