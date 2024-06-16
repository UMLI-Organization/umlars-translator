from xml.etree import ElementTree as ET
from typing import Iterator

from umlars_translator.core.deserialization.abstract.xml.xml_pipeline import (
    XmlModelProcessingPipe,
    XmlFormatDetectionPipe,
    XmlAttributeCondition,
    DataBatch,
    AliasToXmlKey,
)
from umlars_translator.core.deserialization.formats.ea_xmi.ea_constants import (
    TAGS,
    ATTRIBUTES,
    EA_EXTENDED_TAGS,
    EA_EXTENDED_ATTRIBUTES,
    EA_DIAGRAMS_TYPES,
    EaPackagedElementTypes,
)
from umlars_translator.core.deserialization.exceptions import UnsupportedFormatException


# The following classes are used to detect the format of the data
class EaXmiDetectionPipe(XmlFormatDetectionPipe):
    ASSOCIATED_XML_TAG: str = TAGS["root"]
    EXPECTED_XMI_VERSION: str = "2.1"

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        data_root = self._get_root_element(data, exception_on_parsing_error=UnsupportedFormatException)
        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(xmi_version = ATTRIBUTES["xmi_version"])
        except KeyError as ex:
            raise ValueError(f"Configuration of the data format was invalid. Error: {str(ex)}")

        aliases_to_values = self._get_attributes_values_for_aliases(data_root, mandatory_attributes, exception_on_parsing_error=UnsupportedFormatException)

        if aliases_to_values['xmi_version'] != self.__class__.EXPECTED_XMI_VERSION:
            raise UnsupportedFormatException("Invalid XMI version.")

        # Iteration over the children of the root element
        yield from self._create_data_batches(data_root)


class EaXmiDocumentationDetectionPipe(XmlFormatDetectionPipe):
    ASSOCIATED_XML_TAG: str = TAGS["documentation"]
    EXPECTED_EXPORTER: str = "Enterprise Architect"

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(exporter = ATTRIBUTES["exporter"])
        except KeyError as ex:
            raise ValueError(f"Configuration of the data format was invalid. Error: {str(ex)}")
        
        aliases_to_values = self._get_attributes_values_for_aliases(data, mandatory_attributes, exception_on_parsing_error=UnsupportedFormatException)
        
        if aliases_to_values['exporter'] != self.__class__.EXPECTED_EXPORTER:
            raise UnsupportedFormatException("Invalid exporter.")
        
        yield from self._create_data_batches(data)


# The following classes are used to process the data
class RootPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = TAGS["root"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data_root = self._get_root_element(data_batch.data)
        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(xmi_version = ATTRIBUTES["xmi_version"])
        except KeyError as ex:
            raise ValueError(f"Configuration of the data format was invalid. Error: {str(ex)}")
        
        aliases_to_values = self._get_attributes_values_for_aliases(data_root, mandatory_attributes)
        self.model_builder.construct_metadata(**aliases_to_values)

        # Iteration over the children of the root element
        yield from self._create_data_batches(data_root)


class DocumentationPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = TAGS["documentation"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(exporter = ATTRIBUTES["exporter"])
            optional_attributes = AliasToXmlKey.from_kwargs(exporterVersion = ATTRIBUTES["exporterVersion"], exporterID = ATTRIBUTES["exporterID"])
        except KeyError as ex:
            raise ValueError(f"Configuration of the data format was invalid. Error: {str(ex)}")

        aliases_to_values = self._get_attributes_values_for_aliases(data, mandatory_attributes, optional_attributes)
        self.model_builder.construct_metadata(**aliases_to_values)

        yield from self._create_data_batches(data)


class UmlModelPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = TAGS["model"]
    ATTRIBUTES_CONDITIONS: Iterator[XmlAttributeCondition] = [XmlAttributeCondition(ATTRIBUTES["type"], "uml:Model")]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(name = ATTRIBUTES["name"], visibility = ATTRIBUTES["visibility"])
        except KeyError as ex:
            raise ValueError(f"Configuration of the data format was invalid. Error: {str(ex)}")
        
        aliases_to_values = self._get_attributes_values_for_aliases(data, mandatory_attributes)
        self.model_builder.construct_uml_model(**aliases_to_values)

        yield from self._create_data_batches(data)


class UmlPackagePipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = TAGS["packaged_element"]
    ATTRIBUTES_CONDITIONS: Iterator[XmlAttributeCondition] = [XmlAttributeCondition(ATTRIBUTES["type"], "uml:Package")]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(id = ATTRIBUTES["id"] , name = ATTRIBUTES["name"], visibility = ATTRIBUTES["visibility"])
        except KeyError as ex:
            raise ValueError(f"Configuration of the data format was invalid. Error: {str(ex)}")

        aliases_to_values = self._get_attributes_values_for_aliases(data, mandatory_attributes)
        self.model_builder.construct_uml_package(**aliases_to_values)

        yield from self._create_data_batches(data)


class UmlClassPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = TAGS["packaged_element"]
    ATTRIBUTES_CONDITIONS: Iterator[XmlAttributeCondition] = [XmlAttributeCondition(ATTRIBUTES["type"], EaPackagedElementTypes.CLASS)]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        
        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(name = ATTRIBUTES["name"], visibility = ATTRIBUTES["visibility"])
        except KeyError as ex:
            raise ValueError(f"Configuration of the data format was invalid. Error: {str(ex)}")
        
        aliases_to_values = self._get_attributes_values_for_aliases(data, mandatory_attributes)
        self.model_builder.construct_uml_class(**aliases_to_values)
        
        yield from self._create_data_batches(data)


class UmlInterfacePipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = TAGS["packaged_element"]
    ATTRIBUTES_CONDITIONS: Iterator[XmlAttributeCondition] = [XmlAttributeCondition(ATTRIBUTES["type"], EaPackagedElementTypes.INTERFACE)]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        
        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(name = ATTRIBUTES["name"], visibility = ATTRIBUTES["visibility"])
        except KeyError as ex:
            raise ValueError(f"Configuration of the data format was invalid. Error: {str(ex)}")
        
        aliases_to_values = self._get_attributes_values_for_aliases(data, mandatory_attributes)
        self.model_builder.construct_uml_interface(**aliases_to_values)

        yield from self._create_data_batches(data)


class UmlAttributePipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG: str = TAGS["owned_attribute"]
    ATTRIBUTES_CONDITIONS: Iterator[XmlAttributeCondition] = [XmlAttributeCondition(ATTRIBUTES["type"], "uml:Property")]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                name=ATTRIBUTES["name"],
                id=ATTRIBUTES["id"],
                type=ATTRIBUTES["type"],
            )

            optional_attributes = AliasToXmlKey.from_kwargs(
                visibility=ATTRIBUTES["visibility"],
                is_static=ATTRIBUTES["is_static"],
                is_ordered=ATTRIBUTES["is_ordered"],
                is_unique=ATTRIBUTES["is_unique"],
                is_read_only=ATTRIBUTES["is_read_only"],
                is_query=ATTRIBUTES["is_query"],
                is_derived=ATTRIBUTES["is_derived"],
                is_derived_union=ATTRIBUTES["is_derived_union"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )
        
        aliases_to_values = self._get_attributes_values_for_aliases(data, mandatory_attributes, optional_attributes)
        self.model_builder.construct_uml_attribute(**aliases_to_values)
        
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
            mandatory_attributes = AliasToXmlKey.from_kwargs(id = ATTRIBUTES["id"])
            aliases_to_values = self._get_attributes_values_for_aliases(data, mandatory_attributes)

            diagram_properties = data.find(EA_EXTENDED_TAGS["properties"])

            self._construct_diagram_from_properties(diagram_properties, aliases_to_values["id"])

            diagram_elements = data.find(EA_EXTENDED_TAGS["elements"])
            self._construct_diagram_elements(diagram_elements, aliases_to_values["id"])
        except KeyError as ex:
            raise ValueError(f"Configuration of the data format was invalid. Error: {str(ex)}")

        yield from self._create_data_batches(data)

    def _construct_diagram_from_properties(self, diagram_properties: ET.Element, diagram_id: str) -> None:
        optional_attributes = AliasToXmlKey.from_kwargs(
            diagram_type = EA_EXTENDED_ATTRIBUTES["property_type"],
            diagram_name = EA_EXTENDED_ATTRIBUTES["element_name"],
        )
        aliases_to_values = self._get_attributes_values_for_aliases(diagram_properties, optional_attributes)
        self.model_builder.construct_diagram(**aliases_to_values, id=diagram_id)
        
    def _construct_diagram_elements(self, diagram_elements: ET.Element, diagram_id: str) -> None:
        for element in diagram_elements:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                element_id = EA_EXTENDED_ATTRIBUTES["subject"],
            )
            aliases_to_values = self._get_attributes_values_for_aliases(element, mandatory_attributes)

            self.model_builder.bind_element_to_diagram(element_id=aliases_to_values["element_id"], diagram_id=diagram_id)