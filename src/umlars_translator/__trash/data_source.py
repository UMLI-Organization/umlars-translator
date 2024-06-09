import json
from typing import Union

from umlars_translator.core.abstract.deserializer.json.exceptions import InvalidJsonException

class JsonDataSource:
    def __init__(self, data: Union[dict, str]) -> None:
        try:
            self._data = data if isinstance(data, dict) else json.loads(data)
        except json.JSONDecodeError as e:
            raise InvalidJsonException("The data is not a valid JSON format.") from e

    @property
    def data(self) -> Any:
        return self._data
    
    @data.setter
    def data(self, data: Any) -> None:
        self._data = data
