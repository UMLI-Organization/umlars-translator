from xml.etree import ElementTree as ET
from typing import Callable, Iterator, Optional, NamedTuple, Any

from umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline import (
    ModelProcessingPipe,
    UmlModelBuilder,
    FormatDetectionPipe,
    DataBatch,
)
from umlars_translator.core.deserialization.exceptions import InvalidFormatException


class AliasToXmlKey(NamedTuple):
    alias: str
    xml_key: str

    @classmethod
    def from_kwargs(cls, **kwargs) -> Iterator["AliasToXmlKey"]:
        return (cls(alias=alias, xml_key=xml_key) for alias, xml_key in kwargs.items())


class XmlAttributeCondition(NamedTuple):
    attribute_name: str
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


class XmlModelProcessingPipe(ModelProcessingPipe):
    ASSOCIATED_XML_TAG: Optional[str] = None
    ATTRIBUTES_CONDITIONS: Optional[Iterator[XmlAttributeCondition | Callable]] = None

    @classmethod
    def get_associated_xml_tag(cls) -> str:
        return cls.ASSOCIATED_XML_TAG

    @classmethod
    def get_attributes_conditions(
        cls,
    ) -> Optional[Iterator[XmlAttributeCondition | Callable]]:
        return cls.ATTRIBUTES_CONDITIONS

    def __init__(
        self,
        xml_tag: Optional[str] = None,
        attributes_conditions: Optional[
            Iterator[XmlAttributeCondition | Callable]
        ] = None,
        successors: Optional[Iterator["ModelProcessingPipe"]] = None,
        predecessor: Optional["ModelProcessingPipe"] = None,
        model_builder: Optional[UmlModelBuilder] = None,
    ) -> None:
        self._associated_xml_tag = xml_tag or self.__class__.get_associated_xml_tag()
        self._attributes_conditions = self._create_attributes_conditions_callables(
            attributes_conditions
        )
        super().__init__(successors, predecessor, model_builder)

    def _create_attributes_conditions_callables(
        self,
        custom_attributes_conditions: Optional[
            Iterator[XmlAttributeCondition | Callable]
        ],
    ) -> Iterator[XmlAttributeCondition | Callable]:
        attributes_conditions = []
        if custom_attributes_conditions is not None:
            attributes_conditions.extend(custom_attributes_conditions)

        if (
            class_attributes_conditions := self.__class__.get_attributes_conditions()
        ) is not None:
            attributes_conditions.extend(class_attributes_conditions)

        return [
            self._create_attribute_condition_callable(condition)
            for condition in attributes_conditions
        ]

    def _create_attribute_condition_callable(
        self, attribute_condition: XmlAttributeCondition | Callable
    ) -> Callable:
        if isinstance(attribute_condition, XmlAttributeCondition):
            return attribute_condition.to_callable()
        return attribute_condition

    def _has_required_attributes_values(
        self, data: ET.ElementTree | ET.Element
    ) -> bool:
        if not self._attributes_conditions:
            return True

        return all(condition(data) for condition in self._attributes_conditions)

    def _can_process(self, data_batch: Optional[DataBatch] = None) -> bool:
        data: ET.ElementTree | ET.Element = data_batch.data

        if isinstance(data, ET.ElementTree):
            data = self._get_root_element(data)

        try:
            return (
                data.tag == self._associated_xml_tag or self._associated_xml_tag is None
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
        exception_on_parsing_error: type = InvalidFormatException,
    ) -> dict[str,str]:
        kwargs = {}
        try:
            if mandatory_attributes is not None:
                try:
                    for alias, xml_key in mandatory_attributes:
                        kwargs[alias] = data.attrib[xml_key]
                except KeyError as ex:
                    raise exception_on_parsing_error(
                        f"Structure of the data format was invalid. Error: {str(ex)}"
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
            raise exception_on_parsing_error(error_message) from ex

        return kwargs

    def _get_root_element(
        self,
        data: ET.ElementTree,
        exception_on_parsing_error: type = InvalidFormatException,
    ) -> ET.Element:
        try:
            return data.getroot()
        except AttributeError as ex:
            error_message = f"Xml processing pipeline didn't receive parsed xml data. Received: {data} of type {type(data)}"
            self._logger.error(error_message)
            raise exception_on_parsing_error(error_message) from ex


    def _map_value_from_key(
        self,
        values_dict: dict[str, str],
        key_to_map: str,
        mapping_dict: dict[str, Any],
    ) -> str:
        try:
            value_to_map = values_dict[key_to_map]
            values_dict[key_to_map] = mapping_dict[value_to_map]
        except KeyError as ex:
            raise InvalidFormatException(
                f"Value {value_to_map} not found in mapping dict {mapping_dict}" 
                f"or key {key_to_map} not found in values dict {values_dict}."
            ) from ex
        
class XmlFormatDetectionPipe(XmlModelProcessingPipe, FormatDetectionPipe):
    """
    Diamond inheiritance.
    """
