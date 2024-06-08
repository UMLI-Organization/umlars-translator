from abc import ABC, abstractmethod
from typing import Optional

from umlars_translator.core.deserializer.config import SupportedFormat
from umlars_translator.core.deserializer.abstract.base.data_source import DataSource

class DeserializationStrategy(ABC):
    SUPPORTED_FORMAT_NAME: Optional[SupportedFormat] = None
    """
    Used dunder static attribute to store the supported format name and don't share it with subclasses. 
    """

    @staticmethod
    @abstractmethod
    def get_supported_format() -> SupportedFormat:
        """
        Abstract method enforcing the implementation of a property to return the supported format name.
        """
        pass

    
    @abstractmethod
    @staticmethod
    def can_deserialize_format(format: Optional[SupportedFormat] = None, format_data: Optional[DataSource]) -> bool:
        """
        Method used by a final user to check if a specific format can be deserialized.
        Uses self._can_deserialize_format_data and self.__class__.__SUPPORTED_FORMAT_NAME to check if the format is supported.
        """
        pass

    @abstractmethod
    @staticmethod
    def _can_deserialize_format_data(format_data: Optional[DataSource]) -> bool:
        """
        Helper method used to check if the format data is valid for deserialization.
        """
        pass

    @abstractmethod
    def retrieve_model(self, data_source: DataSource) -> UMLModel:
        pass

