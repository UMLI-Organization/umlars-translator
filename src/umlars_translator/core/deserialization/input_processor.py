from logging import Logger
from typing import Optional, Iterator
from abc import ABC

from kink import inject

from umlars_translator.core.deserialization.data_source import DataSource


@inject
class InputProcessor:
    
    def __init__(self, logger: Optional[Logger]=None) -> None:
        self._logger = logger.getChild(self.__class__.__name__)

    def accept_input(self, data: Optional[str] = None, file_path: Optional[str] = None) -> DataSource:
        if data is not None:
            yield self.parse_data(data=data)

    def accept_multiple_inputs(self, data_batches: Optional[Iterator[str]] = None, file_paths_list: Optional[Iterator[str]] = None) -> Iterator[DataSource]:
        if data_batches is not None:
            self._logger.info("Accepting multiple data batches")
            yield from (self.parse_data(data=data_batch) for data_batch in data_batches)
        
        if file_paths_list is not None:
            self._logger.info("Accepting multiple file paths")
            yield from (self.parse_data(file_path=file_path) for file_path in file_paths_list)


    def parse_data(self, data: Optional[str]=None, file_path: Optional[str]=None) -> DataSource:
        """
        Method should be extended by the subclasses. It allows adjustment of the approach to data retrieval
        """
        return DataSource(data=data, file_path=file_path)