from typing import Optional

from umlars_translator.core.deserialization.data_source import DataSource
from umlars_translator.core.deserialization.abstract.base.deserialization_strategy import (
    DeserializationStrategy,
)
from umlars_translator.core.deserialization.factory import (
    register_deserialization_strategy,
)
from umlars_translator.core.deserialization.abstract.iterable_format.format_iterator import (
    XmlIterator,
)
from umlars_translator.core.model.uml_model import UMLModel
from umlars_translator.core.deserialization.config import SupportedFormat


class ElementBuilder:
    """ """


class TypeToBuilderMapper:
    """ """


@register_deserialization_strategy
class EaXmiImportParsingStrategy(DeserializationStrategy):
    SUPPORTED_FORMAT_NAME = SupportedFormat.XMI_EA

    def retrieve_model(self, source: DataSource) -> UMLModel:
        print("Retrieving EA XMI")
        return list(XmlIterator().iterate(source))

    @classmethod
    def get_supported_format(cls: type["DeserializationStrategy"]) -> SupportedFormat:
        """
        Abstract method enforcing the implementation of a property to return the supported format name.
        """
        return cls.SUPPORTED_FORMAT_NAME

    def can_deserialize_format(
        self,
        format: Optional[SupportedFormat] = None,
        format_data: Optional[DataSource] = None,
    ) -> bool:
        """
        Method used by a final user to check if a specific format can be deserialized.
        Uses self._can_deserialize_format_data and self.__class__.__SUPPORTED_FORMAT_NAME to check if the format is supported.
        """
        return True

    def _can_deserialize_format_data(self, format_data: Optional[DataSource]) -> bool:
        """
        Helper method used to check if the format data is valid for deserialization.
        """
        pass
