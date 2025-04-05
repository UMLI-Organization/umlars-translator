from typing import Optional, Iterable
from logging import Logger

from kink import inject

from umlars_translator.core.deserialization.deserializer import ModelDeserializer
from umlars_translator.core.serialization.umlars_model.json_serializer import UmlToPydanticSerializer
from umlars_translator.core.serialization.abstract.serializer import UmlSerializer
from umlars_translator.config import SupportedFormat
from umlars_translator.core.deserialization.data_source import DataSource
from umlars_translator.core.model.abstract.uml_model import IUmlModel


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
        self._model = model_to_extend or model_deseializer.model

    def translate(
        self,
        data: Optional[str] = None,
        file_name: Optional[str] = None,
        file_paths: Optional[Iterable[str]] = None,
        data_batches: Optional[Iterable[str]] = None,
        data_sources: Optional[Iterable[DataSource]] = None,
        from_format: Optional[SupportedFormat] = None,
        model_to_extend: Optional[IUmlModel] = None,
        clear_model_afterwards: bool = False,
        model_id: Optional[str] = None,
        to_string: bool = True,
    ) -> str | Iterable[str]:
        deserialized_model: IUmlModel = self.deserialize(
            data, file_name, file_paths, data_batches, data_sources, from_format, model_to_extend, clear_builder_afterwards=clear_model_afterwards, model_id=model_id
        )
        # TODO: serializer should accept many implementations of IUmlModel
        serialized_model = self.serialize(deserialized_model, to_string=to_string)
        return serialized_model

    def deserialize(
        self,
        data: Optional[str] = None,
        file_name: Optional[str] = None,
        file_paths: Optional[Iterable[str]] = None,
        data_batches: Optional[Iterable[str]] = None,
        data_sources: Optional[Iterable[DataSource]] = None,
        from_format: Optional[SupportedFormat] = None,
        model_to_extend: Optional[IUmlModel] = None,
        model_id: Optional[str] = None,
        clear_builder_afterwards: bool = False,
    ) -> IUmlModel:
        self._logger.info("Deserializing model")

        model_to_extend = model_to_extend or self._model
    
        if model_id is not None:
            self._logger.info(f"Model ID will be set to {model_id}")
            model_to_extend.id = model_id

        if data is not None:
            deserialized_model = self._model_deserializer.deserialize(data_batches=[data], from_format=from_format, model_to_extend=model_to_extend, clear_builder_afterwards=True)

        elif file_name is not None:
            deserialized_model = self._model_deserializer.deserialize(file_paths=[file_name], from_format=from_format, model_to_extend=model_to_extend, clear_builder_afterwards=True)

        else:
            deserialized_model = self._model_deserializer.deserialize(file_paths, data_batches, data_sources, from_format=from_format, model_to_extend=model_to_extend, clear_builder_afterwards=True)

        self._logger.info("Model deserialized")

        if clear_builder_afterwards:
            self.clear()
        else:
            self._model = deserialized_model

        return deserialized_model

    @inject
    def serialize(self, model: Optional[IUmlModel] = None, serializer: Optional[UmlSerializer] = None, to_string: bool = True) -> str:
        model = model or self._model
        self._logger.info("Serializing model")
        serialized_model = serializer.serialize(model, to_string=to_string)
        self._logger.info("Model serialized")
        return serialized_model
    
    def clear(self) -> None:
        self._model = None
        self._model_deserializer.clear()
        self._logger.info("Model cleared")
