from typing import Any


class DataSource:
    def __init__(self, data: Any) -> None:
        self._data = data

    @property
    def data(self) -> Any:
        return self._data

    @data.setter
    def data(self, data: Any) -> None:
        self._data = data
