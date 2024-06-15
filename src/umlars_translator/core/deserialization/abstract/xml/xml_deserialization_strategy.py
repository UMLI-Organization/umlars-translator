from typing import Any
from xml.etree import ElementTree as ET

from umlars_translator.core.model.uml_model import UMLModel
from umlars_translator.core.deserialization.data_source import DataSource
from umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline_deserialization_strategy import (
    PipelineDeserializationStrategy,
)
from umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline import (
    ModelProcessingPipe,
)


class XmlDeserializationStrategy(PipelineDeserializationStrategy):
    def _parse_format_data(self, data_source: DataSource) -> Any:
        return self.get_element_tree(data_source)

    def get_element_tree(self, source: DataSource) -> ET.ElementTree:
        return (
            ET.parse(source.file_path)
            if source.file_path is not None
            else ET.ElementTree(ET.fromstring(source.retrieved_data))
        )


class XmiDeserializationStrategy(XmlDeserializationStrategy):
    ...
