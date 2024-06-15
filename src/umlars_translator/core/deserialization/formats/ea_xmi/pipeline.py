from xml.etree import ElementTree as ET
from enum import Enum
from typing import Callable, Iterator, Optional, NamedTuple, Any

from umlars_translator.core.deserialization.abstract.xml.pipeline import XmlModelProcessingPipe, XmlFormatDetectionPipe
from umlars_translator.core.deserialization.formats.ea_xmi.constants import TAGS, ATTRIBUTES
from umlars_translator.core.deserialization.exceptions import UnsupportedFormatException


class EaXmiDetectionPipe(XmlFormatDetectionPipe):
    ASSOCIATED_XML_TAG: str = TAGS["root"]
    EXPECTED_XMI_VERSION: str = "2.1"

    def _process(self, data: ET.ElementTree) -> Iterator[ET.Element]:
        try:
            data_root = data.getroot()
            xmi_version = data_root.attrib[ATTRIBUTES["xmi_version"]]
        except AttributeError as ex:
            raise UnsupportedFormatException(f"Structure of the data format was invalid. Error: {str(ex)}") from ex
        
        except KeyError as ex:
            raise UnsupportedFormatException(f"Structure of the data format was invalid. Error: {str(ex)}") from ex

        if xmi_version != self.__class__.EXPECTED_XMI_VERSION:
            raise UnsupportedFormatException(f"Invalid XMI version.")

        # Iteration over the children of the root element
        yield from data_root


class EaXmiDocumentationDetectionPipe(XmlFormatDetectionPipe):
    ASSOCIATED_XML_TAG: str = TAGS["documentation"]
    EXPECTED_EXPORTER: str = "Enterprise Architect"

    def _process(self, data: ET.Element) -> Iterator[ET.Element]:
        try:
            exporter = data.attrib[ATTRIBUTES["exporter"]]
        except KeyError as ex:
            raise ValueError(f"Structure of the data format was invalid. Error: {str(ex)}")

        if exporter != self.__class__.EXPECTED_EXPORTER:
            raise UnsupportedFormatException(f"Invalid exporter.")
        yield from data


class RootPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = TAGS["root"]

    def _process(self, data: ET.ElementTree) -> Iterator[ET.Element]:
        data_root = data.getroot()
        try:
            self.model_builder.xmi_version(data_root.attrib[ATTRIBUTES["xmi_version"]])
        except KeyError as ex:
            raise ValueError(f"Structure of the data format was invalid. Error: {str(ex)}")
        
        # Iteration over the children of the root element
        yield from data_root
        

class DocumentationPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = TAGS["documentation"]

    def _process(self, data: ET.Element) -> Iterator[ET.Element]:
        try:
            self.model_builder.documentation(data.attrib[ATTRIBUTES["exporter"]], data.attrib[ATTRIBUTES["exporterVersion"]], data.attrib[ATTRIBUTES["exporterID"]])
        except KeyError as ex:
            raise ValueError(f"Structure of the data format was invalid. Error: {str(ex)}")

        yield from data


class ModelPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = TAGS["model"]

    def _process(self, data: ET.Element) -> Iterator[ET.Element]:
        try:
            self.model_builder.model(data.attrib[ATTRIBUTES["name"]], data.attrib[ATTRIBUTES["name"]], data.attrib[ATTRIBUTES["visibility"]])
        except KeyError as ex:
            raise ValueError(f"Structure of the data format was invalid. Error: {str(ex)}")

        yield from data