import re
from typing import Iterator, Optional, Callable, NamedTuple
from dataclasses import dataclass

from umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline import (
    DataBatch,
    FormatDetectionPipe,
    ModelProcessingPipe
)
from umlars_translator.core.deserialization.exceptions import InvalidFormatException


class AliasToJSONKey(NamedTuple):
    alias: str
    json_key: str

    @classmethod
    def from_kwargs(cls, **kwargs) -> Iterator["AliasToJSONKey"]:
        return (cls(alias=alias, json_key=json_key) for alias, json_key in kwargs.items())


@dataclass
class JSONAttributeCondition:
    attribute_name: str
    expected_value: str
    when_missing_raise_exception: bool = False
    regexp: bool = False

    def to_callable(self) -> Callable:
        def attribute_condition(data: dict) -> bool:
            try:
                if self.regexp:
                    return re.match(self.expected_value, data[self.attribute_name])
                return data[self.attribute_name] == self.expected_value
            except KeyError as ex:
                if self.when_missing_raise_exception:
                    raise InvalidFormatException(
                        f"Attribute {self.attribute_name} not found in data {data}"
                    ) from ex
                return False
            except AttributeError as ex:
                raise InvalidFormatException(
                    f"JSON attribute condition didn't receive parsed JSON data. Received: {data} of type {type(data)}"
                ) from ex

        return attribute_condition
    
    @classmethod
    def from_regex(cls, attribute_name: str, expected_value: str) -> "JSONAttributeCondition":
        return cls(attribute_name=attribute_name, expected_value=expected_value, regexp=True)


class JSONModelProcessingPipe(ModelProcessingPipe):
    ATTRIBUTE_CONDITIONS: Optional[Iterator[JSONAttributeCondition]] = None

    @classmethod
    def get_attribute_conditions(cls) -> Iterator[JSONAttributeCondition]:
        return cls.ATTRIBUTE_CONDITIONS or []

    def _can_process(self, data_batch: Optional[DataBatch] = None) -> bool:
        data: dict = data_batch.data

        try:
            return self._has_required_attributes_values(data)
        except AttributeError as ex:
            error_message = f"Unexpected error occurred while processing JSON data. Received: {data} of type {type(data)}"
            self._logger.error(error_message)
            raise InvalidFormatException(error_message) from ex

    def _has_required_attributes_values(self, data: dict) -> bool:
        for condition in self.get_attribute_conditions():
            if not condition.to_callable()(data):
                return False
        return True

    def _get_attributes_values_for_aliases(
        self,
        data: dict,
        mandatory_attributes: Optional[Iterator[AliasToJSONKey]] = None,
        optional_attributes: Optional[Iterator[AliasToJSONKey]] = None,
    ) -> dict[str, str]:
        kwargs = {}
        try:
            if mandatory_attributes is not None:
                try:
                    for alias, json_key in mandatory_attributes:
                        kwargs[alias] = data[json_key]
                except KeyError as ex:
                    raise InvalidFormatException(
                        f"Structure of the data format was invalid. Missing key {json_key}. Error: {str(ex)}"
                    )

            if optional_attributes is not None:
                for alias, json_key in optional_attributes:
                    value = data.get(json_key)
                    if value is not None:
                        kwargs[alias] = value

        except AttributeError as ex:
            if not isinstance(data, dict):
                error_message = f"Xml processing pipeline didn't receive parsed JSON data. Received: {data} of type {type(data)}"
            else:
                error_message = f"Unexpected error occurred while processing JSON data. Received: {data} of type {type(data)}"
            self._logger.error(error_message)
            raise InvalidFormatException(error_message) from ex

        return kwargs


class JSONFormatDetectionPipe(FormatDetectionPipe, JSONModelProcessingPipe):
    ...
