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
from umlars_translator.core.model.constants import UmlDiagramType, UmlVisibilityEnum


class PapyrusXmiModelProcessingPipe(XmlModelProcessingPipe):
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
            self.config.PAPYRUS_TYPE_ATTRIBUTE_MAPPING,
            raise_when_missing=False,
        )
        self._process_type_metadata(aliases_to_values)

        return aliases_to_values

    def _process_type_metadata(self, aliases_to_values: dict[str, Any]) -> None:
        aliases_to_values["type_metadata"] = {}
        self._map_value_from_key(
            aliases_to_values,
            "href",
            self.config.PAPYRUS_HREF_ATTRIBUTE_MAPPING,
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
                type=self.config.ATTRIBUTES["type"],
            )
            optional_attributes = AliasToXmlKey.from_kwargs(
                value=self.config.ATTRIBUTES["value"],
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            lower_value_data, mandatory_attributes, optional_attributes
        )

        self._map_value_from_key(
            aliases_to_values, "type", self.config.PAPYRUS_TYPE_ATTRIBUTE_MAPPING
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
            aliases_to_values, "type", self.config.PAPYRUS_TYPE_ATTRIBUTE_MAPPING
        )

        return aliases_to_values


class UmlModelPipe(PapyrusXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["model"]
    # TODO: take value from config
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(Config.ATTRIBUTES["type"], "uml:Model")
    ]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data
        data_root = self._get_root_element(data)

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                name=self.config.ATTRIBUTES["name"],
                xmi_version=self.config.ATTRIBUTES["xmi_version"]

            )
            optional_attributes = AliasToXmlKey.from_kwargs(
                visibility=self.config.ATTRIBUTES["visibility"]
            )
        except KeyError as ex:
            raise ValueError(
                f"Configuration of the data format was invalid. Error: {str(ex)}"
            )

        aliases_to_values = self._get_attributes_values_for_aliases(
            data_root, mandatory_attributes, optional_attributes
        )

        self._map_value_from_key(
            aliases_to_values, "visibility", {None: UmlVisibilityEnum.PUBLIC}, raise_when_missing=False
        )

        self.model_builder.construct_metadata(xmi_version=aliases_to_values.pop("xmi_version"))

        self.model_builder.construct_uml_model(**aliases_to_values)

        yield from self._create_data_batches(data_root)


class UmlClassPipe(PapyrusXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["packaged_element"]
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(
            Config.ATTRIBUTES["type"], Config.PapyrusPackagedElementTypes.CLASS
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
        
        self._map_value_from_key(
            aliases_to_values, "visibility", {None: UmlVisibilityEnum.PUBLIC}, raise_when_missing=False
        )

        self.model_builder.construct_uml_class(**aliases_to_values)
        if "package_id" in data_batch.parent_context:
            self.model_builder.add_class_to_package(class_id=aliases_to_values["id"], package_id=data_batch.parent_context["package_id"])

        yield from self._create_data_batches(data, parent_context={"parent_id": aliases_to_values["id"]})


class UmlInterfacePipe(PapyrusXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["packaged_element"]
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(
            Config.ATTRIBUTES["type"], Config.PapyrusPackagedElementTypes.INTERFACE
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


class UmlAttributePipe(PapyrusXmiModelProcessingPipe):
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


class UmlOperationPipe(PapyrusXmiModelProcessingPipe):
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


class UmlOperationParameterPipe(PapyrusXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["operation_parameter"]

    def _process(self, data_batch: DataBatch) -> Iterator[DataBatch]:
        data = data_batch.data

        try:
            mandatory_attributes = AliasToXmlKey.from_kwargs(
                id=self.config.ATTRIBUTES["id"],
            )

            optional_attributes = AliasToXmlKey.from_kwargs(
                name=self.config.ATTRIBUTES["name"],
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
                aliases_to_values, "type", self.config.PAPYRUS_TYPE_ATTRIBUTE_MAPPING
            )
        except UnableToMapError:
            type_attr_value = aliases_to_values.pop("type")
            if type_attr_value is not None:
                self._logger.debug(
                    f"Assuming type attribute value: {type_attr_value} is an ID reference."
                )
                aliases_to_values["type_id"] = type_attr_value

        aliases_to_values.update(self._process_type_child(data_batch))

        self.model_builder.construct_uml_operation_parameter(
            **aliases_to_values, operation_id=data_batch.parent_context["parent_id"]
        )
        yield from self._create_data_batches(
            data, parent_context={"parent_id": aliases_to_values["id"]}
        )


class UmlDataTypePipe(PapyrusXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["packaged_element"]
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(
            Config.ATTRIBUTES["type"], Config.PapyrusPackagedElementTypes.DATA_TYPE
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

        self._map_value_from_key(
            aliases_to_values, "visibility", {None: UmlVisibilityEnum.PUBLIC}, raise_when_missing=False
        )

        self.model_builder.construct_uml_data_type(**aliases_to_values)
        if "package_id" in data_batch.parent_context:
            self.model_builder.add_data_type_to_package(data_type_id=aliases_to_values["id"], package_id=data_batch.parent_context["package_id"])

        yield from self._create_data_batches(
            data, parent_context={"parent_id": aliases_to_values["id"]}
        )


class UmlEnumerationPipe(PapyrusXmiModelProcessingPipe):
    ASSOCIATED_XML_TAG = Config.TAGS["packaged_element"]
    ATTRIBUTES_CONDITIONS = [
        XmlAttributeCondition(
            Config.ATTRIBUTES["type"], Config.PapyrusPackagedElementTypes.ENUMERATION
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

        self._map_value_from_key(
            aliases_to_values, "visibility", {None: UmlVisibilityEnum.PUBLIC}, raise_when_missing=False
        )

        self.model_builder.construct_uml_enumeration(**aliases_to_values)
        if "package_id" in data_batch.parent_context:
            self.model_builder.add_enumeration_to_package(enumeration_id=aliases_to_values["id"], package_id=data_batch.parent_context["package_id"])

        yield from self._create_data_batches(
            data, parent_context={"parent_id": aliases_to_values["id"]}
        )


class UmlAssociationPipe(PapyrusXmiModelProcessingPipe):
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
                member_ends_string=self.config.ATTRIBUTES["member_end"],
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

        member_ends = aliases_to_values.pop("member_ends_string")
        self.model_builder.construct_uml_association(**aliases_to_values)
        if "package_id" in data_batch.parent_context:
            self.model_builder.add_association_to_package(association_id=aliases_to_values["id"], package_id=data_batch.parent_context["package_id"])

        self._process_member_ends(member_ends, association_id=aliases_to_values["id"])

        yield from self._create_data_batches(
            data, parent_context={"parent_id": aliases_to_values["id"]}
        )

    def _process_member_ends(self, member_ends_string: str | None, association_id: str) -> None:
        if member_ends_string is None:
            return
        
        member_ends = member_ends_string.split(" ")
        for member_end in member_ends:
            self.model_builder.bind_end_to_association(
                end_id=member_end, association_id=association_id
            )
            # TODO: it should register call for function that will set element to element from given If that element isnt AssociationEnd. Otherwise it would just set that ASsociationEnd to Association


class UmlAssociationOwnedEndPipe(PapyrusXmiModelProcessingPipe):
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

