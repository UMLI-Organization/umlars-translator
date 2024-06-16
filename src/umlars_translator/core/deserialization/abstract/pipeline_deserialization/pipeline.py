from abc import ABC, abstractmethod
from typing import Optional, Callable, NamedTuple, Any, Iterator
from logging import Logger

from kink import inject

from umlars_translator.core.deserialization.exceptions import (
    UnsupportedFormatException,
)
from umlars_translator.core.model.uml_model import UmlModel
from umlars_translator.core.model.uml_model_builder import UmlModelBuilder


class DataBatch(NamedTuple):
    """
    Represents a batch of data to be processed by a pipe.
    Parent context is a dictionary of data shared from the predecessor pipe.
    Dictionary is used to allow flexible information exchange.
    """
    data: Any
    parent_context: Optional[dict[str, Any]] = None



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

    def process_if_possible(self, data: Optional[Any] = None, parent_context: Optional[dict[str, Any]] = None, data_batch: Optional[DataBatch] = None) -> None:
        data_batch = DataBatch(data, parent_context) if data_batch is None else data_batch

        if self.can_run_for(data_batch=data_batch):
            self.process(data_batch=data_batch)

    def process(self, data: Optional[Any] = None, parent_context: Optional[dict[str, Any]] = None, data_batch: Optional[DataBatch] = None) -> None:
        data_batch = DataBatch(data, parent_context) if data_batch is None else data_batch
            
        batches_of_data_processed_by_parent = self._process(data_batch=data_batch)
        
        # It is a generator so iteration through it can be done only once.
        # TODO: this should be optimized not to iterate through all successors for each data batch IF some way of grouping successors is possible.
        for data_batch in batches_of_data_processed_by_parent:
            for successor in self._successors:
                successor.process_if_possible(data_batch=data_batch)

    def get_model(self) -> UmlModel:
        return self.model_builder.build()

    def can_run_for(self, data: Optional[Any] = None, parent_context: Optional[dict[str, Any]] = None, data_batch: Optional[DataBatch] = None) -> bool:
        data_batch = DataBatch(data, parent_context) if data_batch is None else data_batch
        return self._can_process(data_batch=data_batch)
    
    def _create_data_batches(self, data_iterator: Iterator[Any], parent_context: Optional[dict[str, Any]] = None, **kwargs) -> Iterator[DataBatch]:
        if parent_context is None:
            parent_context = {}
        parent_context.update(kwargs)

        yield from (DataBatch(data, parent_context) for data in data_iterator)

    @abstractmethod
    def _process(self, data_batch: Optional[DataBatch] = None) -> Iterator[DataBatch]:
        """
        Processes the accepted data in a way defined by the subclass. Returns data splitted into parts to be processed by successor pipes.
        Throws InvalidFormatException if the data is not valid for the pipe. It can be avoided by checking the data before processing using can_run_for method.
        """
        ...

    @abstractmethod
    def _can_process(self, data_batch: Optional[DataBatch] = None) -> bool:
        """
        Method overrided in each subclass. Defines, whether the received data can be parsed by default pipe of such type.
        """


class FormatDetectionPipe(ModelProcessingPipe):
    def is_supported_format(self, data: Optional[Any] = None, parent_context: Optional[dict[str, Any]] = None, data_batch: Optional[DataBatch] = None) -> bool:
        data_batch = DataBatch(data, parent_context) if data_batch is None else data_batch
        
        if not self.can_run_for(data_batch=data_batch):
            return False

        try:
            self.process(data_batch=data_batch)
            return True
        except UnsupportedFormatException as ex:
            self._logger.debug(f"Format is not supported: {ex}")
            return False

    @abstractmethod
    def _process(self, data_batch: Optional[DataBatch] = None) -> Iterator[DataBatch]:
        """
        Throws UnsupportedFormatException if the format indicators are invalid in regards to the represented format.
        """
