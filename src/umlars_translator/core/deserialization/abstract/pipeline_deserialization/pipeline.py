from abc import ABC, abstractmethod
from typing import Optional, NamedTuple, Any, Iterator, Callable
from logging import Logger

from kink import inject

from umlars_translator.core.deserialization.exceptions import (
    InvalidFormatException,
    UnsupportedFormatException,
    ImproperlyInstantiatedObjectError,
    UnableToMapError,
)
from umlars_translator.core.model.abstract.uml_model import IUmlModel
from umlars_translator.core.model.abstract.uml_model_builder import IUmlModelBuilder
from umlars_translator.core.configuration.config_namespace import ConfigNamespace


def require_instantiated_builder(method: Callable) -> Callable:
    def inner(self: "ModelProcessingPipe", *args, **kwargs) -> Any:
        if self.model_builder is None:
            error_message = f"Method {method.__name__} requires the builder attribute to contain the properly instantiated UmlModelBuilder. Error in class: {self.__class__.__name__}"
            self._logger.error(error_message)
            raise ImproperlyInstantiatedObjectError(error_message)
        return method(self, *args, **kwargs)

    return inner


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
        model_builder: IUmlModelBuilder | None = None,
        config: Optional[ConfigNamespace] = None,
        core_logger: Optional[Logger] = None,
    ) -> None:
        self._logger = core_logger.getChild(self.__class__.__name__)
        self._successors = successors if successors is not None else []
        self._predecessor = predecessor
        self._model_builder = model_builder
        self.set_config(config)

    @property
    def model_builder(self) -> IUmlModelBuilder:
        return self._model_builder

    @property
    def predecessor(self) -> Optional["ModelProcessingPipe"]:
        return self._predecessor

    @predecessor.setter
    def predecessor(self, new_predecessor: Optional["ModelProcessingPipe"]) -> None:
        self._predecessor = new_predecessor

    @property
    def config(self) -> dict[str, Any]:
        return self._config

    def set_model_builder(
        self,
        new_model_builder: Optional[ConfigNamespace],
        update_successors: bool = True,
    ) -> None:
        """
        Updates the config of the pipeline and all its successors.
        """
        self._model_builder = new_model_builder

        if update_successors:
            for successor in self._successors:
                # In case of circular dependencies, the successor can be the same object as the predecessor.
                if successor is not self:
                    successor.set_model_builder(new_model_builder)

    def set_config(
        self,
        new_config: Optional[ConfigNamespace],
        update_successors: bool = True,
        configure: bool = True,
    ) -> None:
        """
        Updates the config of the pipeline and all its successors.
        """
        self._config = new_config

        if configure:
            self._configure()

        if update_successors:
            for successor in self._successors:
                # In case of circular dependencies, the successor can be the same object as the predecessor.
                if successor is not self:
                    successor.set_config(new_config)

    def add_next(
        self,
        pipe: "ModelProcessingPipe",
        share_builder: bool = True,
        share_config: bool = True,
    ) -> "ModelProcessingPipe":
        self._successors.append(pipe)
        if share_builder:
            pipe.set_model_builder(self.model_builder, update_successors=True)

        if share_config:
            pipe.set_config(self.config, update_successors=True)

        pipe.add_predecessor(self)
        return pipe

    def add_predecessor(self, pipe: "ModelProcessingPipe") -> "ModelProcessingPipe":
        if self not in pipe._successors:
            pipe.add_next(self)
        self._predecessor = pipe

    def process_if_possible(
        self,
        data: Optional[Any] = None,
        parent_context: Optional[dict[str, Any]] = None,
        data_batch: Optional[DataBatch] = None,
    ) -> None:
        data_batch = (
            DataBatch(data, parent_context) if data_batch is None else data_batch
        )

        if self.can_run_for(data_batch=data_batch):
            self.process(data_batch=data_batch)

    def process(
        self,
        data: Optional[Any] = None,
        parent_context: Optional[dict[str, Any]] = None,
        data_batch: Optional[DataBatch] = None,
    ) -> None:
        data_batch = (
            DataBatch(data, parent_context) if data_batch is None else data_batch
        )

        batches_of_data_processed_by_parent = self._process(data_batch=data_batch)

        # It is a generator so iteration through it can be done only once and has to be done exactly ones to make the operations execute.
        # TODO: this should be optimized not to iterate through all successors for each data batch IF some way of grouping successors is possible.
        for data_batch in batches_of_data_processed_by_parent:
            for successor in self._successors:
                successor.process_if_possible(data_batch=data_batch)

    @require_instantiated_builder
    def get_model(self) -> IUmlModel:
        return self.model_builder.build()

    def can_run_for(
        self,
        data: Optional[Any] = None,
        parent_context: Optional[dict[str, Any]] = None,
        data_batch: Optional[DataBatch] = None,
    ) -> bool:
        data_batch = (
            DataBatch(data, parent_context) if data_batch is None else data_batch
        )
        return self._can_process(data_batch=data_batch)

    def _create_data_batches(
        self,
        data_iterator: Iterator[Any],
        parent_context: Optional[dict[str, Any]] = None,
        **kwargs,
    ) -> Iterator[DataBatch]:
        if parent_context is None:
            parent_context = {}
        parent_context.update(kwargs)

        yield from (DataBatch(data, parent_context) for data in data_iterator)

    def _map_value_from_key(
        self,
        values_dict: dict[str, str],
        key_to_map: str,
        mapping_dict: dict[str, Any],
        raise_when_missing: bool = True,
        inplace: bool = True,
    ) -> str | None:
        value_to_map = None
        try:
            value_to_map = values_dict[key_to_map]
            mapped_value = mapping_dict[value_to_map]
            if inplace:
                values_dict[key_to_map] = mapped_value
            else:
                return mapped_value

        except KeyError as ex:
            if raise_when_missing:
                raise UnableToMapError(
                    f"Value {value_to_map} not found in mapping dict"
                    f"or key {key_to_map} not found in values dict."
                ) from ex
            return None

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

    def _configure(self) -> None:
        """
        Configures the pipe using the config namespace.
        Run always whenever the config is set and flag configure is set to True.
        Should be overriden in subclasses if needed.
        """


class FormatDetectionPipe(ModelProcessingPipe):
    def is_supported_format(
        self,
        data: Optional[Any] = None,
        parent_context: Optional[dict[str, Any]] = None,
        data_batch: Optional[DataBatch] = None,
    ) -> bool:
        data_batch = (
            DataBatch(data, parent_context) if data_batch is None else data_batch
        )

        if not self.can_run_for(data_batch=data_batch):
            return False

        try:
            self.process(data_batch=data_batch)
            return True
        except InvalidFormatException as ex:
            self._logger.debug(
                f"Format is not invalid - pipeline processing failed: {ex}"
            )
            return False
        except UnsupportedFormatException as ex:
            self._logger.debug(f"Format is not supported: {ex}")
            return False
