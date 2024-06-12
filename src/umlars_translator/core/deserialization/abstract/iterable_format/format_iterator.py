import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Iterator

from umlars_translator.core.deserialization.data_source import DataSource
from umlars_translator.core.deserialization.abstract.iterable_format.iteration_step_element import (
    FormatElement,
)


class FormatIterator(ABC):
    @abstractmethod
    def iterate(self, source: DataSource) -> Iterator[FormatElement]:
        pass


class JsonIterator(FormatIterator):
    def iterate(self, source: DataSource) -> Iterator[FormatElement]:
        pass


class XmlIterator(FormatIterator):
    def iterate(self, source: DataSource) -> Iterator[FormatElement]:
        element_tree = self.get_element_tree(source)
        for element in self.iterate_elements(element_tree):
            yield element

    def get_element_tree(self, source: DataSource) -> ET.ElementTree:
        return (
            ET.parse(source.file_path)
            if source.file_path is not None
            else ET.ElementTree(ET.fromstring(source.retrieved_data))
        )

    def iterate_elements(self, element_tree: ET.ElementTree) -> Iterator[FormatElement]:
        yield from element_tree.iter()
