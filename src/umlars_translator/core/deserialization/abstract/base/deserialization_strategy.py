from abc import ABC, abstractmethod
from typing import Optional
from logging import Logger

from kink import inject

from umlars_translator.core.deserialization.config import SupportedFormat
from umlars_translator.core.deserialization.data_source import DataSource
from umlars_translator.core.model.uml_model import UmlModel
from umlars_translator.core.configuration.config_namespace import ConfigNamespace


@inject
class DeserializationStrategy(ABC):
    """
    Class should be lightweight since it will be often instantiated for checking, if it can deserialize data.
    """

    SUPPORTED_FORMAT_NAME: SupportedFormat
    # TODO: improve this config approach - currently deserialization strategy has too much of a responsibility - some ConfigManager with dependency injection could be used
    CONFIG_NAMESPACE_CLASS: type["ConfigNamespace"]

    def __init__(self, logger: Optional[Logger] = None, config_namespace: Optional[ConfigNamespace] = None) -> None:
        self._logger = logger.getChild(self.__class__.__name__)
        self._config = config_namespace if config_namespace is not None else self.__class__.get_config_namespace_class()()

    @property
    def config(self) -> ConfigNamespace:
        return self._config

    @classmethod
    def get_supported_format(cls: type["DeserializationStrategy"]) -> SupportedFormat:
        return cls.SUPPORTED_FORMAT_NAME

    @classmethod
    def get_config_namespace_class(cls: type["DeserializationStrategy"]) -> type["ConfigNamespace"]:
        return cls.CONFIG_NAMESPACE_CLASS

    def can_deserialize_format(
        self,
        format: Optional[SupportedFormat] = None,
        format_data: Optional[DataSource] = None,
    ) -> bool:
        """
        Method used by a final user to check if a specific format can be deserialized.
        Uses self._can_deserialize_format_data and self.__class__.__SUPPORTED_FORMAT_NAME to check if the format is supported.
        """
        return (
            format is self.__class__.get_supported_format()
            or self._can_deserialize_format_data(format_data)
        )

    @abstractmethod
    def _can_deserialize_format_data(self, format_data: DataSource) -> bool:
        """
        Helper method used to check if the format data is valid for deserialization.
        """

    @abstractmethod
    def retrieve_model(self, data_source: DataSource) -> UmlModel:
        """
        Method resposible for the main processing of the source data.
        It performs the transformations required to retrieve all the data from source format into the UML Model.
        """
