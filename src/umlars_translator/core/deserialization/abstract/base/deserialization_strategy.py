from abc import ABC, abstractmethod
from typing import Optional

from umlars_translator.core.deserialization.config import SupportedFormat
from umlars_translator.core.deserialization.data_source import DataSource
from umlars_translator.core.model.uml_model import UMLModel


class DeserializationStrategy(ABC):
    SUPPORTED_FORMAT_NAME: Optional[SupportedFormat]
    """
    Used dunder static attribute to store the supported format name and don't share it with subclasses. 
    """

    @classmethod
    @abstractmethod
    def get_supported_format(cls: type["DeserializationStrategy"]) -> SupportedFormat:
        """
        Abstract method enforcing the implementation of a property to return the supported format name.
        """

    @abstractmethod
    def can_deserialize_format(self, format: Optional[SupportedFormat] = None, format_data: Optional[DataSource] = None) -> bool:
        """
        Method used by a final user to check if a specific format can be deserialized.
        Uses self._can_deserialize_format_data and self.__class__.__SUPPORTED_FORMAT_NAME to check if the format is supported.
        """

    @abstractmethod
    def _can_deserialize_format_data(self, format_data: Optional[DataSource]) -> bool:
        """
        Helper method used to check if the format data is valid for deserialization.
        """

    @abstractmethod
    def retrieve_model(self, data_source: DataSource) -> UMLModel:
        pass

