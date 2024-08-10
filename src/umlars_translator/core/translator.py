from typing import Optional, Iterable
from logging import Logger

from kink import inject

from src.umlars_translator.core.deserialization.deserializer import ModelDeserializer
from src.umlars_translator.config import SupportedFormat
from src.umlars_translator.core.deserialization.data_source import DataSource
from src.umlars_translator.core.model.abstract.uml_model import IUmlModel


@inject
class ModelTranslator:
    def __init__(
        self,
        model_deseializer: Optional[ModelDeserializer] = None,
        core_logger: Optional[Logger] = None,
        model_to_extend: Optional[IUmlModel] = None,
    ) -> None:
        self._model_deserializer = model_deseializer
        self._logger = core_logger.getChild(self.__class__.__name__)
        self._logger.info("ModelTranslator initialized")
        self._model = model_to_extend

    def translate(
        self,
        data: Optional[str] = None,
        file_name: Optional[str] = None,
        file_paths: Optional[Iterable[str]] = None,
        data_batches: Optional[Iterable[str]] = None,
        data_sources: Optional[Iterable[DataSource]] = None,
        from_format: Optional[SupportedFormat] = None,
        model_to_extend: Optional[IUmlModel] = None,
    ) -> str | Iterable[str]:
        deserialized_model: IUmlModel = self.deserialize(
            data, file_name, file_paths, data_batches, data_sources, from_format, model_to_extend
        )
        # TODO: serialize
        return deserialized_model


    def deserialize(
        self,
        data: Optional[str] = None,
        file_name: Optional[str] = None,
        file_paths: Optional[Iterable[str]] = None,
        data_batches: Optional[Iterable[str]] = None,
        data_sources: Optional[Iterable[DataSource]] = None,
        from_format: Optional[SupportedFormat] = None,
        model_to_extend: Optional[IUmlModel] = None,
    ) -> IUmlModel:
        self._logger.info("Deserializing model")

        model_to_extend = model_to_extend or self._model

        if data is not None:
            deserialized_model = self._model_deserializer.deserialize(data_batches=[data], from_format=from_format, model_to_extend=model_to_extend, clear_builder_afterwards=True)

        elif file_name is not None:
            deserialized_model = self._model_deserializer.deserialize(file_paths=[file_name], from_format=from_format, model_to_extend=model_to_extend, clear_builder_afterwards=True)

        else:
            deserialized_model = self._model_deserializer.deserialize(file_paths, data_batches, data_sources, from_format=from_format, model_to_extend=model_to_extend, clear_builder_afterwards=True)

        self._logger.info("Model deserialized")

        self._model = deserialized_model

        return self._model
