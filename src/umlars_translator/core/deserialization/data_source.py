from typing import Any, Callable, Optional, Iterable
from functools import cached_property


class DataSource:
    def __init__(
        self, data: Optional[str | Callable] = None, file_path: Optional[str] = None
    ) -> None:
        self._data = data
        self._file_path = file_path

    @cached_property
    def retrieved_data(self) -> str:
        """
        Returns data stored in the data property.
        If it contains None value or Callable - the data is extracted and then returned.
        """
        if isinstance(self._data, Callable):
            return self._data()

        if self._data is None:
            if self._file_path is not None:
                return self.read_data_from_file()
        else:
            return self._data

        raise ValueError("Tried to access data that wasn't properly setup")

    @property
    def data(self) -> str:
        return self._data

    @data.setter
    def data(self, data: str | Callable) -> None:
        self._data = data

    @property
    def file_path(self) -> str:
        return self._file_path

    @file_path.setter
    def file_path(self, file_path: str) -> None:
        self._file_path = file_path

    @cached_property
    def data_by_lines(self) -> Iterable[str]:
        with open(self._file_path, "r", encoding="utf-8") as file:
            yield from file.readlines()

    def read_data_from_file(self) -> str:
        with open(self._file_path, "r", encoding="utf-8") as file:
            return file.read()
