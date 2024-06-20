import importlib
from typing import Optional, Iterator, Dict, Iterator, TYPE_CHECKING
from logging import Logger

from kink import inject

from umlars_translator.core.deserialization.input_processor import InputProcessor
from umlars_translator.core.deserialization.data_source import DataSource
from umlars_translator.core.deserialization.config import SupportedFormat
from umlars_translator.core.model.abstract.uml_model import IUmlModel
from umlars_translator.core.extensions_manager import ExtensionsManager
from umlars_translator.core.deserialization import config
from umlars_translator.core.deserialization.factory import (
    DeserializationStrategyFactory,
)
from umlars_translator.core.deserialization.abstract.base.deserialization_strategy import (
    DeserializationStrategy,
)
from umlars_translator.core.model.abstract.uml_model_builder import IUmlModelBuilder


@inject
class ModelDeserializer:
    def __init__(
        self,
        factory: DeserializationStrategyFactory,
        deserialization_extensions_manager: ExtensionsManager,
        input_processor: Optional[InputProcessor] = None,
        model_builder: Optional[IUmlModelBuilder] = None,
        logger: Optional[Logger] = None,
    ) -> None:
        self._factory = factory
        self._deserialization_extensions_manager = deserialization_extensions_manager
        self._model_builder = model_builder
        self._input_processor = input_processor or InputProcessor()
        self._logger = logger.getChild(self.__class__.__name__)
        self.load_formats_support()

    def load_formats_support(
        self, extensions_group_name: Optional[Iterator[str]] = None
    ) -> None:
        if extensions_group_name is None:
            extensions_group_name = config.DESERIALIZATION_EXTENSIONS_GROUP_NAME
        self._deserialization_extensions_manager.activate_extensions(
            extensions_group_name
        )

    def deserialize(
        self,
        file_paths: Optional[Iterator[str]] = None,
        data_batches: Optional[Iterator[str]] = None,
        data_sources: Optional[Iterator[DataSource]] = None,
        from_format: Optional[SupportedFormat] = None,
    ) -> Iterator[IUmlModel]:
        """
        TODO: Support for accepting dictionary assigning from_format to file_name or data_batch.
        """
        self._logger.info(
            f"Deserializing model for data batches: {data_batches} and file paths: {file_paths}"
        )
        if not data_sources:
            data_sources = self._input_processor.accept_multiple_inputs(
                data_batches, file_paths
            )
            self._logger.info("Multiple inputs accepted.")

        self._logger.info("Deserializing data sources")
        yield from self.deserialize_data_sources(data_sources, from_format)

    def deserialize_data_sources(
        self,
        data_sources: Iterator[DataSource],
        from_format: Optional[SupportedFormat] = None,
    ) -> Iterator[IUmlModel]:
        for source in data_sources:
            self._logger.info(
                f"Choosing deserialization strategy for data source: {source}"
            )
            import_parsing_strategy = self.get_strategy_for_source(source, from_format)
            self._logger.info(f"Retrieving model from data source: {source}")
            yield import_parsing_strategy.retrieve_model(source)

    def get_strategy_for_source(
        self, source: DataSource, from_format: Optional[SupportedFormat] = None
    ) -> DeserializationStrategy:
        return self._factory.get_strategy(
            format_data_source=source,
            format=from_format,
            model_builder=self._model_builder,
        )
