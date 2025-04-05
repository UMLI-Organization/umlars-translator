from xml.etree import ElementTree as ET
from typing import Callable, Iterator, Optional, NamedTuple, Any
from dataclasses import dataclass

from umlars_translator.core.model.abstract.uml_model_builder import IUmlModelBuilder
from umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline import (
    ModelProcessingPipe,
    FormatDetectionPipe,
    DataBatch,
)
from umlars_translator.core.deserialization.exceptions import (
    InvalidFormatException,
)
from umlars_translator.core.configuration.config_namespace import ParsedConfigNamespace
from umlars_translator.core.configuration.config_proxy import (
    ConfigProxy,
    get_configurable_value,
)


class AliasToXmlKey(NamedTuple):
    alias: str
    xml_key: str

    @classmethod
    def from_kwargs(cls, **kwargs) -> Iterator["AliasToXmlKey"]:
        return (cls(alias=alias, xml_key=xml_key) for alias, xml_key in kwargs.items())


@dataclass
class XmlAttributeCondition:
    attribute_name: str | ConfigProxy
    expected_value: Any
    when_missing_raise_exception: bool = False

    def to_callable(self) -> Callable:
        def attribute_condition(xml_element: ET.Element) -> bool:
            try:
                return xml_element.attrib[self.attribute_name] == self.expected_value
            except KeyError as ex:
                if self.when_missing_raise_exception:
                    raise InvalidFormatException(
                        f"Attribute {self.attribute_name} not found in xml element {xml_element}"
                    ) from ex
                return False
            # TODO: add tests for this behavior
            except AttributeError as ex:
                raise InvalidFormatException(
                    f"Xml attribute condition didn't receive parsed xml data. Received: {xml_element} of type {type(xml_element)}"
                ) from ex

        return attribute_condition

    def evaluate_attribute_condition(self, config: ParsedConfigNamespace) -> None:
        self.attribute_name = get_configurable_value(self.attribute_name, config)
        self.expected_value = get_configurable_value(self.expected_value, config)


class XmlModelProcessingPipe(ModelProcessingPipe):
    ASSOCIATED_XML_TAG: Optional[str | ConfigProxy] = None
    ATTRIBUTES_CONDITIONS: Optional[Iterator[XmlAttributeCondition | Callable]] = None

    @classmethod
    def get_attributes_conditions(
        cls,
    ) -> Optional[Iterator[XmlAttributeCondition | Callable]]:
        return cls.ATTRIBUTES_CONDITIONS

    @classmethod
    def get_associated_xml_tag(cls) -> str:
        return cls.ASSOCIATED_XML_TAG

    def __init__(
        self,
        xml_tag: Optional[str] = None,
        attributes_conditions: Optional[
            Iterator[XmlAttributeCondition | Callable]
        ] = None,
        successors: Optional[Iterator["ModelProcessingPipe"]] = None,
        predecessor: Optional["ModelProcessingPipe"] = None,
        model_builder: Optional[IUmlModelBuilder] = None,
        config: Optional[ParsedConfigNamespace] = None,
        **kwargs,
    ) -> None:
        self._associated_xml_tag = (
            xml_tag if xml_tag is not None else self.__class__.get_associated_xml_tag()
        )
        self._attributes_conditions = (
            attributes_conditions
            if attributes_conditions is not None
            else self.__class__.get_attributes_conditions()
        )
        super().__init__(successors, predecessor, model_builder, config, **kwargs)

    def _configure(self) -> None:
        if self._config is not None:
            self._configure_xml_tag()
            self._configure_attributes_conditions_callables()

    def _configure_xml_tag(self) -> None:
        if self._associated_xml_tag is not None:
            self._associated_xml_tag = get_configurable_value(
                self._associated_xml_tag, self.config
            )

    def _configure_attributes_conditions_callables(
        self,
    ) -> Iterator[XmlAttributeCondition | Callable]:
        if self._attributes_conditions is not None:
            self._attributes_conditions = [
                self._configure_attribute_condition_callable(condition)
                for condition in self._attributes_conditions
            ]

    def _configure_attribute_condition_callable(
        self, attribute_condition: XmlAttributeCondition | Callable
    ) -> Callable:
        if isinstance(attribute_condition, XmlAttributeCondition):
            attribute_condition.evaluate_attribute_condition(self.config)
            return attribute_condition.to_callable()
        return attribute_condition

    def _has_required_attributes_values(
        self, data: ET.ElementTree | ET.Element
    ) -> bool:
        if not self._attributes_conditions:
            return True

        return all(condition(data) for condition in self._attributes_conditions)

    @staticmethod
    def _are_tags_matching(tag_1: str, tag_2: str) -> bool:
        # URI is not parsed in the same way by the ElementTree always
        # When the same XMI file was parsed with deleted <elements>, <primitiveTypes> and <profiles> - ET suddenly started to add '/' at the end of the URI
        tag_1 = tag_1.replace('/}', '}')
        tag_2 = tag_2.replace('/}', '}')
        return (tag_1 == tag_2)

    def _can_process(self, data_batch: Optional[DataBatch] = None) -> bool:
        data: ET.ElementTree | ET.Element = data_batch.data

        if isinstance(data, ET.ElementTree):
            data = self._get_root_element(data)

        try:
            return (
                self._associated_xml_tag is None or self._are_tags_matching(data.tag, self._associated_xml_tag)
            ) and self._has_required_attributes_values(data)
        except AttributeError as ex:
            if not isinstance(data, ET.Element):
                error_message = f"Xml processing pipeline didn't receive parsed xml data. Received: {data} of type {type(data)}"
            else:
                error_message = f"Unexpected error occurred while processing xml data. Received: {data} of type {type(data)}"

            self._logger.error(error_message)
            raise InvalidFormatException(error_message) from ex

    def _get_attributes_values_for_aliases(
        self,
        data: ET.Element,
        mandatory_attributes: Optional[Iterator[AliasToXmlKey]] = None,
        optional_attributes: Optional[Iterator[AliasToXmlKey]] = None,
    ) -> dict[str, str]:
        kwargs = {}
        try:
            if mandatory_attributes is not None:
                try:
                    for alias, xml_key in mandatory_attributes:
                        kwargs[alias] = data.attrib[xml_key]
                except KeyError as ex:
                    raise InvalidFormatException(
                        f"Structure of the data format was invalid. Missing key {xml_key}. Error: {str(ex)}"
                    )

            if optional_attributes is not None:
                for alias, xml_key in optional_attributes:
                    kwargs[alias] = data.get(xml_key)

        except AttributeError as ex:
            if not isinstance(data, ET.Element):
                error_message = f"Xml processing pipeline didn't receive parsed xml data. Received: {data} of type {type(data)}"
            else:
                error_message = f"Unexpected error occurred while processing xml data. Received: {data} of type {type(data)}"
            self._logger.error(error_message)
            raise InvalidFormatException(error_message) from ex

        return kwargs

    def _get_root_element(
        self,
        data: ET.ElementTree,
    ) -> ET.Element:
        try:
            return data.getroot()
        except AttributeError as ex:
            error_message = f"Xml processing pipeline didn't receive parsed xml data. Received: {data} of type {type(data)}"
            self._logger.error(error_message)
            raise InvalidFormatException(error_message) from ex


class XmlFormatDetectionPipe(FormatDetectionPipe, XmlModelProcessingPipe):
    """
    Diamond inheiritance.
    """
