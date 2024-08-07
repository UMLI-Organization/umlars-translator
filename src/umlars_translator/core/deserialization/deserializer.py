from typing import Optional, Iterator, Dict, Iterator
from logging import Logger

from kink import inject

from src.umlars_translator.core.deserialization.input_processor import InputProcessor
from src.umlars_translator.core.deserialization.data_source import DataSource
from src.umlars_translator.config import SupportedFormat
from src.umlars_translator.core.model.abstract.uml_model import IUmlModel
from src.umlars_translator.core.extensions_manager import ExtensionsManager
from src.umlars_translator.core.deserialization import config
from src.umlars_translator.core.deserialization.factory import (
    DeserializationStrategyFactory,
)
from src.umlars_translator.core.deserialization.abstract.base.deserialization_strategy import (
    DeserializationStrategy,
)
from src.umlars_translator.core.model.abstract.uml_model_builder import IUmlModelBuilder
from src.umlars_translator.core.model.umlars_model.umlars_uml_model_builder import UmlModelBuilder


@inject
class ModelDeserializer:
    def __init__(
        self,
        factory: DeserializationStrategyFactory,
        deserialization_extensions_manager: ExtensionsManager,
        input_processor: Optional[InputProcessor] = None,
        model_builder: IUmlModelBuilder | None = None,
        core_logger: Optional[Logger] = None,
    ) -> None:
        self._factory = factory
        self._deserialization_extensions_manager = deserialization_extensions_manager
        self._model_builder = model_builder or UmlModelBuilder()
        self._input_processor = input_processor or InputProcessor()
        self._logger = core_logger.getChild(self.__class__.__name__)
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
        model_to_extend: Optional[IUmlModel] = None,
        clear_builder_afterwards: bool = True,
    ) -> IUmlModel:
        """
        TODO: Support for accepting dictionary assigning from_format to file_name or data_batch.
        """
        self._logger.info(
            f"Deserializing model for data batches: {data_batches} and file paths: {file_paths}"
        )
        if not data_sources:
            data_sources = self._input_processor.accept_multiple_inputs(
                data_batches, file_paths, format_for_all=from_format
            )
            self._logger.info("Multiple inputs accepted.")

        self._logger.info("Deserializing data sources")
        return self.deserialize_data_sources(data_sources, model_to_extend, clear_builder_afterwards)

    def deserialize_data_sources(
        self,
        data_sources: Iterator[DataSource],
        model_to_extend: Optional[IUmlModel] = None,
        clear_builder_afterwards: bool = True,
    ) -> IUmlModel:
        model: IUmlModel = model_to_extend

        for source in data_sources:
            self._logger.info(
                f"Choosing deserialization strategy for data source: {source}"
            )
            import_parsing_strategy = self.get_strategy_for_source(source)
            self._logger.info(f"Retrieving model from data source: {source}")
            model = import_parsing_strategy.retrieve_model(source, model, self._model_builder, clear_afterwards=False)

        if clear_builder_afterwards:
            self._model_builder.clear()

        return model


    def get_strategy_for_source(
        self, source: DataSource
    ) -> DeserializationStrategy:
        return self._factory.get_strategy(
            format_data_source=source,
            model_builder=self._model_builder,
        )

    def clear(self) -> None:
        self._model_builder.clear()