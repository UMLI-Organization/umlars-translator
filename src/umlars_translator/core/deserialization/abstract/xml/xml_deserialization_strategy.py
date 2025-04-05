from abc import abstractmethod
from typing import Any
from xml.etree import ElementTree as ET

from umlars_translator.core.configuration.config_namespace import ParsedConfigNamespace, ConfigNamespace
from umlars_translator.core.deserialization.abstract.base.deserialization_strategy import DeserializationStrategy
from umlars_translator.core.deserialization.data_source import DataSource
from umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline_deserialization_strategy import (
    PipelineDeserializationStrategy,
)
from umlars_translator.core.deserialization.exceptions import InvalidFormatException
from umlars_translator.core.configuration.config_namespace import ParsedConfigNamespace
from umlars_translator.core.deserialization.abstract.xml.utils import retrieve_namespaces


class XmlDeserializationStrategy(PipelineDeserializationStrategy):
    CONFIG_NAMESPACE_CLASS = ParsedConfigNamespace

    def _parse_format_data(self, data_source: DataSource) -> Any:
        """
        Parse the data from the data source and return the parsed data.
        TODO: To improve - now it has the side effect of parsing the config - too much responsibility and not obvoius what the function does.
        """
        try:
            self._parse_config(data_source)
            return self._get_element_tree(data_source)
        except ET.ParseError as ex:
            error_message = f"Error parsing XML data from {data_source}: {ex}"
            self._logger.warning(error_message)
            raise InvalidFormatException(error_message)

    def _get_element_tree(self, source: DataSource) -> ET.ElementTree:
        return (
            ET.parse(source.file_path)
            if source.file_path is not None
            else ET.ElementTree(ET.fromstring(source.retrieved_data))
        )

    def _parse_config(self, source: DataSource) -> ParsedConfigNamespace:
        namespaces = retrieve_namespaces(source)
        return self.config.parse(namespaces)


class XmiDeserializationStrategy(XmlDeserializationStrategy):
    ...
