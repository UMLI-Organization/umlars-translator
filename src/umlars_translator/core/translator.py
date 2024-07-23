from typing import Optional, Iterable
from logging import Logger

from kink import inject

from src.umlars_translator.core.deserialization.deserializer import ModelDeserializer
from src.umlars_translator.core.deserialization.config import SupportedFormat
from src.umlars_translator.core.deserialization.data_source import DataSource


@inject
class ModelTranslator:
    def __init__(
        self,
        model_deseializer: Optional[ModelDeserializer] = None,
        core_logger: Optional[Logger] = None,
    ) -> None:
        self._model_deserializer = model_deseializer
        self._logger = core_logger.getChild(self.__class__.__name__)
        self._logger.info("ModelTranslator initialized")

        self._models = None

    def translate(
        self,
        data: Optional[str] = None,
        file_name: Optional[str] = None,
        file_paths: Optional[Iterable[str]] = None,
        data_batches: Optional[Iterable[str]] = None,
        data_sources: Optional[Iterable[DataSource]] = None,
        from_format: Optional[SupportedFormat] = None,
    ) -> str | Iterable[str]:
        return self.deserialize(
            data, file_name, file_paths, data_batches, data_sources, from_format
        )

    def deserialize(
        self,
        data: Optional[str] = None,
        file_name: Optional[str] = None,
        file_paths: Optional[Iterable[str]] = None,
        data_batches: Optional[Iterable[str]] = None,
        data_sources: Optional[Iterable[DataSource]] = None,
        from_format: Optional[SupportedFormat] = None,
    ) -> str | Iterable[str]:
        self._logger.info("Deserializing model")

        if data is not None:
            self._models = list(
                self._model_deserializer.deserialize(
                    data_batches=[data], from_format=from_format
                )
            )
            return self._models[0]

        if file_name is not None:
            self._models = list(
                self._model_deserializer.deserialize(
                    file_paths=[file_name], from_format=from_format
                )
            )
            return self._models[0]

        self._models = list(
            self._model_deserializer.deserialize(
                file_paths, data_batches, data_sources, from_format
            )
        )

        self._logger.info("Model deserialized")

        return self._models
