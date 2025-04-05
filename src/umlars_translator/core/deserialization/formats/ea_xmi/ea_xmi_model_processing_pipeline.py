from xml.etree import ElementTree as ET
from typing import Iterator, Any

from umlars_translator.core.deserialization.abstract.xml.xml_pipeline import (
    XmlModelProcessingPipe,
    XmlAttributeCondition,
    DataBatch,
    AliasToXmlKey,
)
from umlars_translator.core.deserialization.exceptions import UnableToMapError
from umlars_translator.core.configuration.config_proxy import Config, get_configurable_value
from umlars_translator.core.model.constants import UmlDiagramType


class EaXmiModelProcessingPipe(XmlModelProcessingPipe):
    def _process_type_child(self, data_batch: DataBatch) -> dict[str, Any]:
        data = data_batch.data
        attribute_type_data = data.find(self.config.TAGS["type"])
        if attribute_type_data is None:
            return {}

        try:
            optional_attributes = AliasToXmlKey.from_kwargs(
                href=self.config.ATTRIBUTES["href"],
                idref=self.config.ATTRIBUTES["idref"],
                type=self.config.ATTRIBUTES["type"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            attribute_type_data, optional_attributes=optional_attributes
        )

        self._map_value_from_key(
            aliases_to_values,
            "type",
            self.config.EA_TYPE_ATTRIBUTE_MAPPING,
            raise_when_missing=False,
        )
        self._process_type_metadata(aliases_to_values)

        return aliases_to_values

    def _process_type_metadata(self, aliases_to_values: dict[str, Any]) -> None:
        aliases_to_values["type_metadata"] = {}
        self._map_value_from_key(
            aliases_to_values,
            "href",
            self.config.EA_HREF_ATTRIBUTE_MAPPING,
            raise_when_missing=False,
        )
        aliases_to_values["type_metadata"].update(
            {"referenced_type_href": aliases_to_values.pop("href", None)}
        )
        aliases_to_values["type_metadata"].update(
            {"referenced_type_id": aliases_to_values.pop("idref", None)}
        )

    def _process_attribute_multiplicity(self, data_batch: DataBatch) -> dict[str, Any]:
        return self._process_attribute_lower_value(
            data_batch
        ) | self._process_attribute_upper_value(data_batch)

    def _process_attribute_lower_value(self, data_batch: DataBatch) -> dict[str, Any]:
        data = data_batch.data
        lower_value_data = data.find(self.config.TAGS["lower_value"])
        if lower_value_data is None:
            return {}

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"],
                value=self.config.ATTRIBUTES["value"],
                type=self.config.ATTRIBUTES["type"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            lower_value_data, mandatory_attributes
        )

        self._map_value_from_key(
            aliases_to_values, "type", self.config.EA_TYPE_ATTRIBUTE_MAPPING
        )

        return aliases_to_values

    def _process_attribute_upper_value(self, data_batch: DataBatch) -> dict[str, Any]:
        data = data_batch.data
        upper_value_data = data.find(self.config.TAGS["upper_value"])
        if upper_value_data is None:
            return {}

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"],
                value=self.config.ATTRIBUTES["value"],
                type=self.config.ATTRIBUTES["type"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            upper_value_data, mandatory_attributes
        )
        self._map_value_from_key(
            aliases_to_values, "type", self.config.EA_TYPE_ATTRIBUTE_MAPPING
        )

        return aliases_to_values


class RootPipe(EaXmiModelProcessingPipe):
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


class DocumentationPipe(EaXmiModelProcessingPipe):
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
                f"Configuration of the data format was invalid. Missing key error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )
        self.model_builder.construct_metadata(**aliases_to_values)

        yield from self._create_data_batches(data)


class UmlModelPipe(EaXmiModelProcessingPipe):
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


class UmlPackagePipe(EaXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["packaged_element"]
    # TODO: take value from config
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(Config.ATTRIBUTES["type"], "uml:Package")
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"], name=self.config.ATTRIBUTES["name"]
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

        yield from self._create_data_batches(data, parent_context={"package_id": aliases_to_values["id"]})


class UmlClassPipe(EaXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["packaged_element"]
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(
            Config.ATTRIBUTES["type"], Config.EaPackagedElementTypes.CLASS
        )
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
        self.model_builder.construct_uml_class(**aliases_to_values)
        if "package_id" in data_batch.parent_context:
            self.model_builder.add_class_to_package(class_id=aliases_to_values["id"], package_id=data_batch.parent_context["package_id"])

        yield from self._create_data_batches(data, parent_context={"parent_id": aliases_to_values["id"]})


class UmlInterfacePipe(EaXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["packaged_element"]
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(
            Config.ATTRIBUTES["type"], Config.EaPackagedElementTypes.INTERFACE
        )
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
        self.model_builder.construct_uml_interface(**aliases_to_values)
        if "package_id" in data_batch.parent_context:
            self.model_builder.add_interface_to_package(interface_id=aliases_to_values["id"], package_id=data_batch.parent_context["package_id"])

        yield from self._create_data_batches(data, parent_context={"parent_id": aliases_to_values["id"]})


class UmlAttributePipe(EaXmiModelProcessingPipe):
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

        aliases_to_values.update(self._process_type_child(data_batch))
        aliases_to_values.update(self._process_attribute_multiplicity(data_batch))

        self.model_builder.construct_uml_attribute(**aliases_to_values, classifier_id=data_batch.parent_context["parent_id"])

        yield from self._create_data_batches(
            data, parent_context={"parent_id": aliases_to_values["id"]}
        )


class UmlOperationPipe(EaXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["owned_operation"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"],
                name=self.config.ATTRIBUTES["name"],
            )

            optional_attributes = AliasToXmlKey.from_kwargs(
                visibility=self.config.ATTRIBUTES["visibility"],
                is_static=self.config.ATTRIBUTES["is_static"],
                is_abstract=self.config.ATTRIBUTES["is_abstract"],
                is_unique=self.config.ATTRIBUTES["is_unique"],
                is_ordered=self.config.ATTRIBUTES["is_ordered"],
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

        self.model_builder.construct_uml_operation(**aliases_to_values, classifier_id=data_batch.parent_context["parent_id"])
        yield from self._create_data_batches(
            data, parent_context={"parent_id": aliases_to_values["id"]}
        )


class UmlOperationParameterPipe(EaXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["operation_parameter"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"],
                name=self.config.ATTRIBUTES["name"],
            )

            optional_attributes = AliasToXmlKey.from_kwargs(
                type=self.config.ATTRIBUTES["type"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        try:
            self._map_value_from_key(
                aliases_to_values, "type", self.config.EA_TYPE_ATTRIBUTE_MAPPING
            )
        except UnableToMapError:
            type_attr_value = aliases_to_values.pop("type")
            if type_attr_value is not None:
                self._logger.debug(
                    f"Assuming type attribute value: {type_attr_value} is an ID reference."
                )
                aliases_to_values["type_id"] = type_attr_value

        self.model_builder.construct_uml_operation_parameter(
            **aliases_to_values, operation_id=data_batch.parent_context["parent_id"]
        )
        yield from self._create_data_batches(
            data, parent_context={"parent_id": aliases_to_values["id"]}
        )


class UmlDataTypePipe(EaXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["packaged_element"]
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(
            Config.ATTRIBUTES["type"], Config.EaPackagedElementTypes.DATA_TYPE
        )
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"],
                name=self.config.ATTRIBUTES["name"],
            )

            optional_attributes = AliasToXmlKey.from_kwargs(
                visibility=self.config.ATTRIBUTES["visibility"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self.model_builder.construct_uml_data_type(**aliases_to_values)
        if "package_id" in data_batch.parent_context:
            self.model_builder.add_data_type_to_package(data_type_id=aliases_to_values["id"], package_id=data_batch.parent_context["package_id"])

        yield from self._create_data_batches(
            data, parent_context={"parent_id": aliases_to_values["id"]}
        )


class UmlEnumerationPipe(EaXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["packaged_element"]
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(
            Config.ATTRIBUTES["type"], Config.EaPackagedElementTypes.ENUMERATION
        )
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"],
                name=self.config.ATTRIBUTES["name"],
            )

            optional_attributes = AliasToXmlKey.from_kwargs(
                visibility=self.config.ATTRIBUTES["visibility"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self.model_builder.construct_uml_enumeration(**aliases_to_values)
        if "package_id" in data_batch.parent_context:
            self.model_builder.add_enumeration_to_package(enumeration_id=aliases_to_values["id"], package_id=data_batch.parent_context["package_id"])

        yield from self._create_data_batches(
            data, parent_context={"parent_id": aliases_to_values["id"]}
        )


class UmlAssociationPipe(EaXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["packaged_element"]
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(Config.ATTRIBUTES["type"], "uml:Association")
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"],
            )

            optional_attributes = AliasToXmlKey.from_kwargs(
                name=self.config.ATTRIBUTES["name"],
                visibility=self.config.ATTRIBUTES["visibility"],
                is_derived=self.config.ATTRIBUTES["is_derived"],
                is_derived_union=self.config.ATTRIBUTES["is_derived_union"],
                is_abstract=self.config.ATTRIBUTES["is_abstract"],
                is_query=self.config.ATTRIBUTES["is_query"],
                is_static=self.config.ATTRIBUTES["is_static"],
                is_unique=self.config.ATTRIBUTES["is_unique"],
                is_ordered=self.config.ATTRIBUTES["is_ordered"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes, optional_attributes
        )

        self.model_builder.construct_uml_association(**aliases_to_values)
        if "package_id" in data_batch.parent_context:
            self.model_builder.add_association_to_package(association_id=aliases_to_values["id"], package_id=data_batch.parent_context["package_id"])

        yield from self._create_data_batches(
            data, parent_context={"parent_id": aliases_to_values["id"]}
        )


class UmlAssociationMemberEndPipe(EaXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["member_end"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                idref=self.config.ATTRIBUTES["idref"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data, mandatory_attributes
        )

        self.model_builder.bind_end_to_association(
            end_id=aliases_to_values["idref"],
            association_id=data_batch.parent_context["parent_id"],
        )
        yield from self._create_data_batches(data)


class UmlAssociationOwnedEndPipe(EaXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["owned_end"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"],
                type=self.config.ATTRIBUTES["type"],
            )

            optional_attributes = AliasToXmlKey.from_kwargs(
                name=self.config.ATTRIBUTES["name"],
                role=self.config.ATTRIBUTES["name"],
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

        aliases_to_values.update(self._process_type_child(data_batch))
        aliases_to_values.update(self._process_attribute_multiplicity(data_batch))

        self.model_builder.construct_uml_association_end(
            **aliases_to_values, association_id=data_batch.parent_context["parent_id"]
        )
        yield from self._create_data_batches(
            data, parent_context={"parent_id": aliases_to_values["id"]}
        )


class ExtensionPipe(EaXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["extension"]
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(Config.ATTRIBUTES["extender"], "Enterprise Architect")
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        yield from self._create_data_batches(data)


class DiagramsPipe(EaXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.EA_EXTENDED_TAGS["diagrams"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        yield from self._create_data_batches(data)


class DiagramPipe(EaXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.EA_EXTENDED_TAGS["diagram"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"]
            )
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
        mandatory_attributes = AliasToXmlKey.from_kwargs(
            diagram_type=self.config.EA_EXTENDED_ATTRIBUTES["property_type"],
        )
        optional_attributes = AliasToXmlKey.from_kwargs(
            name=self.config.EA_EXTENDED_ATTRIBUTES["element_name"],
        )
        aliases_to_values = self._get_attributes_values_for_aliases(
            diagram_properties, mandatory_attributes=mandatory_attributes, optional_attributes=optional_attributes
        )

        diagram_type_name = aliases_to_values.pop("diagram_type")

        diagram_type = Config.EA_DIAGRAMS_TYPES_MAPPING[diagram_type_name]
        diagram_type_parsed = get_configurable_value(diagram_type, self.config)

        self._logger.warn(f"Constructing diagram of type: {diagram_type_parsed}")

        match (diagram_type_parsed):
            case UmlDiagramType.CLASS:
                self.model_builder.construct_class_diagram(**aliases_to_values, id=diagram_id)
            case UmlDiagramType.SEQUENCE:
                self.model_builder.construct_sequence_diagram(**aliases_to_values, id=diagram_id)
            case _:
                self._logger.warning(f"Diagram type: {diagram_type_parsed} is not supported.")

    def _construct_diagram_elements(
        self, diagram_elements: ET.Element, diagram_id: str
    ) -> None:
        self._logger.debug(f"Constructing diagram elements for diagram: {diagram_id}")
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
