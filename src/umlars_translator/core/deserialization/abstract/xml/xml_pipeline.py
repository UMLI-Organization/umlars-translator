from xml.etree import ElementTree as ET
from typing import Callable, Iterator, Optional, NamedTuple, Any

from umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline import (
    ModelProcessingPipe,
    UmlModelBuilder,
    FormatDetectionPipe,
    DataBatch,
)
from umlars_translator.core.deserialization.exceptions import InvalidFormatException


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
                raise InvalidFormatException(f"Xml attribute condition didn't receive parsed xml data. Received: {xml_element} of type {type(xml_element)}") from ex

        return attribute_condition


class XmlModelProcessingPipe(ModelProcessingPipe):
    ASSOCIATED_XML_TAG: str
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
            data = data.getroot()
       
        try:
            return (
                data.tag == self._associated_xml_tag
                and self._has_required_attributes_values(data)
            )
        except AttributeError as ex:
            if not isinstance(data, ET.Element):
                error_message = f"Xml processing pipeline didn't receive parsed xml data. Received: {data} of type {type(data)}"
            else:
                error_message = f"Unexpected error occurred while processing xml data. Received: {data} of type {type(data)}"

            self._logger.error(error_message)
            raise InvalidFormatException(error_message) from ex


class XmlFormatDetectionPipe(XmlModelProcessingPipe, FormatDetectionPipe):
    """
    Diamond inheiritance
    """