from xml.etree import ElementTree as ET
from typing import Iterator, Any

from umlars_translator.core.deserialization.abstract.xml.xml_pipeline import (
    XmlModelProcessingPipe,
    XmlFormatDetectionPipe,
    XmlAttributeCondition,
    DataBatch,
    AliasToXmlKey,
)
from umlars_translator.core.deserialization.exceptions import UnsupportedFormatException
from umlars_translator.core.configuration.config_proxy import Config


# The following classes are used to detect the format of the data
class EaXmiDetectionPipe(XmlFormatDetectionPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["root"]
    EXPECTED_XMI_VERSION: str = "2.1"

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        data_root = self._get_root_element(
            data, exception_on_parsing_error=UnsupportedFormatException
        )
        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                xmi_version=self.config.ATTRIBUTES["xmi_version"]
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data_root,
            mandatory_attributes,
            exception_on_parsing_error=UnsupportedFormatException,
        )

        if aliases_to_values["xmi_version"] != self.__class__.EXPECTED_XMI_VERSION:
            raise UnsupportedFormatException("Invalid XMI version.")

        # Iteration over the children of the root element
        yield from self._create_data_batches(data_root)


class EaXmiDocumentationDetectionPipe(XmlFormatDetectionPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["documentation"]
    # TODO: take from config
    EXPECTED_EXPORTER: str = "Enterprise Architect"

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                exporter=self.config.ATTRIBUTES["exporter"]
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data,
            mandatory_attributes,
            exception_on_parsing_error=UnsupportedFormatException,
        )

        if aliases_to_values["exporter"] != self.__class__.EXPECTED_EXPORTER:
            raise UnsupportedFormatException("Invalid exporter.")

        yield from self._create_data_batches(data)


# The following classes are used to process the data

class RootPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["root"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data_root = self._get_root_element(data_batch.data)
        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                xmi_version=self.config.ATTRIBUTES["xmi_version"]
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data_root, mandatory_attributes
        )
        self.model_builder.construct_metadata(**aliases_to_values)

        # Iteration over the children of the root element
        yield from self._create_data_batches(data_root)


class DocumentationPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["documentation"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                exporter=self.config.ATTRIBUTES["exporter"]
            )
            optional_attributes = AliasToXmlKey.from_kwargs(
                exporterVersion=self.config.ATTRIBUTES["exporterVersion"],
                exporterID=self.config.ATTRIBUTES["exporterID"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )
        self.model_builder.construct_metadata(**aliases_to_values)

        yield from self._create_data_batches(data)


class UmlModelPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["model"]
    # TODO: take value from config
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(Config.ATTRIBUTES["type"], "uml:Model")
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                name=self.config.ATTRIBUTES["name"]
            )
            optional_attributes = AliasToXmlKey.from_kwargs(
                visibility=self.config.ATTRIBUTES["visibility"]
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )
        self.model_builder.construct_uml_model(**aliases_to_values)

        yield from self._create_data_batches(data)


class UmlPackagePipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["packaged_element"]
    # TODO: take value from config
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(Config.ATTRIBUTES["type"], "uml:Package")
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"],
                name=self.config.ATTRIBUTES["name"]
            )
            optional_attributes = AliasToXmlKey.from_kwargs(
                visibility=self.config.ATTRIBUTES["visibility"]
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )
        self.model_builder.construct_uml_package(**aliases_to_values)

        yield from self._create_data_batches(data)


class UmlClassPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["packaged_element"]
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(Config.ATTRIBUTES["type"], Config.EaPackagedElementTypes.CLASS)
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                name=self.config.ATTRIBUTES["name"]
            )
            optional_attributes = AliasToXmlKey.from_kwargs(
                visibility=self.config.ATTRIBUTES["visibility"]
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )
        self.model_builder.construct_uml_class(**aliases_to_values)

        yield from self._create_data_batches(data)


class UmlInterfacePipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["packaged_element"]
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(Config.ATTRIBUTES["type"], Config.EaPackagedElementTypes.INTERFACE)
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                name=self.config.ATTRIBUTES["name"]
            )
            optional_attributes = AliasToXmlKey.from_kwargs(
                visibility=self.config.ATTRIBUTES["visibility"]
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )
        self.model_builder.construct_uml_interface(**aliases_to_values)

        yield from self._create_data_batches(data)


class UmlAttributePipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["owned_attribute"]
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(Config.ATTRIBUTES["type"], "uml:Property")
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"],
                type=self.config.ATTRIBUTES["type"],
            )

            optional_attributes = AliasToXmlKey.from_kwargs(
                name=self.config.ATTRIBUTES["name"],
                visibility=self.config.ATTRIBUTES["visibility"],
                is_static=self.config.ATTRIBUTES["is_static"],
                is_ordered=self.config.ATTRIBUTES["is_ordered"],
                is_unique=self.config.ATTRIBUTES["is_unique"],
                is_read_only=self.config.ATTRIBUTES["is_read_only"],
                is_query=self.config.ATTRIBUTES["is_query"],
                is_derived=self.config.ATTRIBUTES["is_derived"],
                is_derived_union=self.config.ATTRIBUTES["is_derived_union"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        aliases_to_values.update(self._process_attribute_type(data_batch))
        aliases_to_values.update(self._process_attribute_multiplicity(data_batch))

        self.model_builder.construct_uml_attribute(**aliases_to_values)
        yield from self._create_data_batches(data, parent_context={"parent_id": aliases_to_values["id"]})

    def _process_attribute_type(self, data_batch: DataBatch) -> dict[str, Any]:
        data = data_batch.data
        attribute_type_data = data.find(self.config.TAGS["type"])
        if attribute_type_data is None:
            return {}
        
        try:
            optional_attributes = AliasToXmlKey.from_kwargs(
                href=self.config.ATTRIBUTES["href"],
                idref=self.config.ATTRIBUTES["idref"],
                type=self.config.ATTRIBUTES["type"]
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            attribute_type_data, optional_attributes=optional_attributes
        )

        self._map_value_from_key(aliases_to_values, "type", self.config.EA_TYPE_ATTRIBUTE_MAPPING, raise_when_missing=False)
        self._process_type_metadata(aliases_to_values)

        return aliases_to_values

    def _process_type_metadata(self, aliases_to_values: dict[str, Any]) -> None:
        aliases_to_values["type_metadata"] = {}
        self._map_value_from_key(aliases_to_values, "href", self.config.EA_HREF_ATTRIBUTE_MAPPING, raise_when_missing=False)
        aliases_to_values["type_metadata"].update({"referenced_type_href": aliases_to_values.pop("href", None)})
        aliases_to_values["type_metadata"].update({"referenced_type_id": aliases_to_values.pop("idref", None)})

    def _process_attribute_multiplicity(self, data_batch: DataBatch) -> dict[str, Any]:
        return self._process_attribute_lower_value(data_batch) | self._process_attribute_upper_value(data_batch)
    
    def _process_attribute_lower_value(self, data_batch: DataBatch) -> dict[str, Any]:
        data = data_batch.data
        lower_value_data = data.find(self.config.TAGS["lower_value"])
        if lower_value_data is None:
            return {}

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"], value=self.config.ATTRIBUTES["value"], type=self.config.ATTRIBUTES["type"]
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            lower_value_data, mandatory_attributes
        )

        self._map_value_from_key(aliases_to_values, "type", self.config.EA_TYPE_ATTRIBUTE_MAPPING)
        
        return aliases_to_values

    def _process_attribute_upper_value(self, data_batch: DataBatch) -> dict[str, Any]:
        data = data_batch.data
        upper_value_data = data.find(self.config.TAGS["upper_value"])
        if upper_value_data is None:
            return {}
        
        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"], value=self.config.ATTRIBUTES["value"], type=self.config.ATTRIBUTES["type"]
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            upper_value_data, mandatory_attributes
        )
        self._map_value_from_key(aliases_to_values, "type", self.config.EA_TYPE_ATTRIBUTE_MAPPING)
        
        return aliases_to_values


class ExtensionPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["extension"]
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(Config.ATTRIBUTES["extender"], "Enterprise Architect")
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        yield from self._create_data_batches(data)


class DiagramsPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.EA_EXTENDED_TAGS["diagrams"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        yield from self._create_data_batches(data)


class DiagramPipe(XmlModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.EA_EXTENDED_TAGS["diagram"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(id=self.config.ATTRIBUTES["id"])
            aliases_to_values = self._get_attributes_values_for_aliases(
                data, mandatory_attributes
            )

            diagram_properties = data.find(self.config.EA_EXTENDED_TAGS["properties"])

            self._construct_diagram_from_properties(
                diagram_properties, aliases_to_values["id"]
            )

            diagram_elements = data.find(self.config.EA_EXTENDED_TAGS["elements"])
            self._construct_diagram_elements(diagram_elements, aliases_to_values["id"])
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        yield from self._create_data_batches(data)

    def _construct_diagram_from_properties(
        self, diagram_properties: ET.Element, diagram_id: str
    ) -> None:
        optional_attributes = AliasToXmlKey.from_kwargs(
            diagram_type=self.config.EA_EXTENDED_ATTRIBUTES["property_type"],
            diagram_name=self.config.EA_EXTENDED_ATTRIBUTES["element_name"],
        )
        aliases_to_values = self._get_attributes_values_for_aliases(
            diagram_properties, optional_attributes
        )
        self.model_builder.construct_diagram(**aliases_to_values, id=diagram_id)

    def _construct_diagram_elements(
        self, diagram_elements: ET.Element, diagram_id: str
    ) -> None:
        for element in diagram_elements:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                element_id=self.config.EA_EXTENDED_ATTRIBUTES["subject"],
            )
            aliases_to_values = self._get_attributes_values_for_aliases(
                element, mandatory_attributes
            )

            self.model_builder.bind_element_to_diagram(
                element_id=aliases_to_values["element_id"], diagram_id=diagram_id
            )
