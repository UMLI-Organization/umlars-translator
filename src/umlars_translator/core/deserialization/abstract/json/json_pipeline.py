from typing import Iterator, Optional, Callable
from dataclasses import dataclass

from src.umlars_translator.core.deserialization.abstract.pipeline_deserialization.pipeline import (
    DataBatch,
    FormatDetectionPipe,
    ModelProcessingPipe
)
from src.umlars_translator.core.deserialization.exceptions import InvalidFormatException


@dataclass
class JSONAttributeCondition:
    attribute_name: str
    expected_value: str
    when_missing_raise_exception: bool = False

    def to_callable(self) -> Callable:
        def attribute_condition(data: dict) -> bool:
            try:
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


class JSONFormatDetectionPipe(FormatDetectionPipe, JSONModelProcessingPipe):
    ...
