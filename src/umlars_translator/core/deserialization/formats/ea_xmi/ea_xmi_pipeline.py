from xml.etree import ElementTree as ET
from enum import Enum
from typing import Callable, Iterator, Optional, NamedTuple, Any

from umlars_translator.core.deserialization.abstract.xml.xml_pipeline import (
    XmlModelProcessingPipe,
    XmlFormatDetectionPipe,
    XmlAttributeCondition,
    DataBatch,
)
from umlars_translator.core.deserialization.formats.ea_xmi.ea_constants import (
    TAGS,
    ATTRIBUTES,
    EA_EXTENDED_TAGS,
    EA_EXTENDED_ATTRIBUTES,
    EA_DIAGRAMS_TYPES,
)
from umlars_translator.core.deserialization.exceptions import UnsupportedFormatException


# The following classes are used to detect the format of the data
class EaXmiDetectionPipe(XmlFormatDetectionPipe):
    ASSOCIATED_XML_TAG: str = TAGS["root"]
    EXPECTED_XMI_VERSION: str = "2.1"

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        try:
            data_root = data.getroot()
            xmi_version = data_root.attrib[ATTRIBUTES["xmi_version"]]
        except AttributeError as ex:
            raise UnsupportedFormatException(
                f"Structure of the data format was invalid. Error: {str(ex)}"
            ) from ex

        except KeyError as ex:
            raise UnsupportedFormatException(
                f"Structure of the data format was invalid. Error: {str(ex)}"
            ) from ex

        if xmi_version != self.__class__.EXPECTED_XMI_VERSION:
            raise UnsupportedFormatException(f"Invalid XMI version.")

        # Iteration over the children of the root element
        yield from self._create_data_batches(data_root)


class EaXmiDocumentationDetectionPipe(XmlFormatDetectionPipe):
    ASSOCIATED_XML_TAG: str = TAGS["documentation"]
    EXPECTED_EXPORTER: str = "Enterprise Architect"

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        try:
            exporter = data.attrib[ATTRIBUTES["exporter"]]
        except KeyError as ex:
            raise ValueError(
                f"Structure of the data format was invalid. Error: {str(ex)}"
            )

        if exporter != self.__class__.EXPECTED_EXPORTER:
            raise UnsupportedFormatException(f"Invalid exporter.")
        yield from self._create_data_batches(data)


# The following classes are used to process the data
class RootPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = TAGS["root"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data_root = data_batch.data.getroot()
        try:
            self.model_builder.construct_metadata(xmi_version=data_root.attrib[ATTRIBUTES["xmi_version"]])
        except KeyError as ex:
            raise ValueError(
                f"Structure of the data format was invalid. Error: {str(ex)}"
            )

        # Iteration over the children of the root element
        yield from self._create_data_batches(data_root)


class DocumentationPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = TAGS["documentation"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        try:
            self.model_builder.construct_metadata(
                exporter=data.attrib[ATTRIBUTES["exporter"]],
                exporterVersion=data.get(ATTRIBUTES["exporterVersion"]),
                exporterID=data.get(ATTRIBUTES["exporterID"]),
            )
        except KeyError as ex:
            raise ValueError(
                f"Structure of the data format was invalid. Error: {str(ex)}"
            )

        yield from self._create_data_batches(data)


class UmlModelPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = TAGS["model"]
    ATTRIBUTES_CONDITIONS: Iterator[XmlAttributeCondition] = [XmlAttributeCondition(ATTRIBUTES["type"], "uml:Model")]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        try:
            self.model_builder.construct_uml_model(
                name=data.attrib[ATTRIBUTES["name"]],
                visibility=data.attrib[ATTRIBUTES["visibility"]],
            )
        except KeyError as ex:
            raise ValueError(
                f"Structure of the data format was invalid. Error: {str(ex)}"
            )

        yield from self._create_data_batches(data)


class UmlPackagePipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = TAGS["packaged_element"]
    ATTRIBUTES_CONDITIONS: Iterator[XmlAttributeCondition] = [XmlAttributeCondition(ATTRIBUTES["type"], "uml:Package")]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        try:
            self.model_builder.construct_uml_package(
                id=data.attrib[ATTRIBUTES["id"]],
                name=data.attrib[ATTRIBUTES["name"]],
                visibility=data.attrib[ATTRIBUTES["visibility"]],
            )
        except KeyError as ex:
            raise ValueError(
                f"Structure of the data format was invalid. Error: {str(ex)}"
            )

        yield from self._create_data_batches(data)


class UmlClassPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = TAGS["packaged_element"]
    ATTRIBUTES_CONDITIONS: Iterator[XmlAttributeCondition] = [XmlAttributeCondition(ATTRIBUTES["type"], "uml:Class")]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        try:
            self.model_builder.construct_uml_class(
                name=data.attrib[ATTRIBUTES["name"]],
                visibility=data.attrib[ATTRIBUTES["visibility"]],
            )
        except KeyError as ex:
            raise ValueError(
                f"Structure of the data format was invalid. Error: {str(ex)}"
            )

        yield from self._create_data_batches(data)







class ExtensionPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = TAGS["extension"]
    ATTRIBUTES_CONDITIONS: Iterator[XmlAttributeCondition] = [XmlAttributeCondition(ATTRIBUTES["extender"], "Enterprise Architect")]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        yield from self._create_data_batches(data)


class DiagramsPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = EA_EXTENDED_TAGS["diagrams"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        yield from self._create_data_batches(data)


class DiagramPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = EA_EXTENDED_TAGS["diagram"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        try:
            diagram_id = data.attrib[ATTRIBUTES["id"]]
            diagram_properties = data.find(EA_EXTENDED_TAGS["properties"])

            self._construct_diagram_from_properties(diagram_properties, diagram_id)

            diagram_elements = data.find(EA_EXTENDED_TAGS["elements"])
            self._construct_diagram_elements(diagram_elements)
        except KeyError as ex:
            raise ValueError(
                f"Structure of the data format was invalid. Error: {str(ex)}"
            )

        yield from self._create_data_batches(data)

    def _construct_diagram_from_properties(self, diagram_properties: ET.Element, diagram_id: str) -> None:
        diagram_type = diagram_properties.attrib.get(EA_EXTENDED_ATTRIBUTES["property_type"])
        diagram_name = diagram_properties.attrib.get(EA_EXTENDED_ATTRIBUTES["element_name"])
        self.model_builder.construct_diagram(
            diagram_id=diagram_id,
            diagram_type=EA_DIAGRAMS_TYPES[diagram_type],
            diagram_name=diagram_name,
        )

    def _construct_diagram_elements(self, diagram_elements: ET.Element) -> None:
        for element in diagram_elements:
            element_id = element.attrib.get(EA_EXTENDED_ATTRIBUTES["subject"])
            self.model_builder.bind_element_to_diagram(element_id=element_id)