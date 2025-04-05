from logging import Logger
from typing import Optional, Iterator, Dict, Any

from kink import inject

from umlars_translator.core.deserialization.data_source import DataSource


@inject
class InputProcessor:
    def __init__(self, core_logger: Optional[Logger] = None) -> None:
        self._logger = core_logger.getChild(self.__class__.__name__)

    def accept_input(
        self, data: Optional[str] = None, file_path: Optional[str] = None,
        format: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> DataSource:
        if data is not None:
            return self.parse_data(data=data, format=format, metadata=metadata, **kwargs)
        
        if file_path is not None:
            return self.parse_data(file_path=file_path, format=format, metadata=metadata, **kwargs)

    def accept_multiple_inputs(
        self,
        data_batches: Optional[Iterator[str]] = None,
        file_paths_list: Optional[Iterator[str]] = None,
        format_for_all: Optional[str] = None,
        formats: Optional[Iterator[str]] = None,
        metadatas: Optional[Iterator[Dict[str, Any]]] = None,
    ) -> Iterator[DataSource]:
        infinite_none_generator = iter(lambda: None, 0)
        metadatas_generator = (metadata for metadata in metadatas) if metadatas is not None else infinite_none_generator
        
        if format_for_all is not None:
            formats_generator = iter(lambda: format_for_all, 0)
        else:
            formats_generator = (format for format in formats) if formats is not None else infinite_none_generator

        if data_batches is not None:
            self._logger.info("Accepting multiple data batches")
            yield from (self.parse_data(data=data_batch, format=format, metadata=metadata) for data_batch, format, metadata in zip(data_batches, formats_generator, metadatas_generator))

        if file_paths_list is not None:
            self._logger.info("Accepting multiple file paths")
            yield from (
                self.parse_data(file_path=file_path,  format=format, metadata=metadata) for file_path, format, metadata in zip(file_paths_list, formats_generator, metadatas_generator)
            )

    def parse_data(
        self, data: Optional[str] = None, file_path: Optional[str] = None, format: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None, **kwargs
    ) -> DataSource:
        """
        Method should be extended by the subclasses. It allows adjustment of the approach to data retrieval
        """
        return DataSource(data=data, file_path=file_path, format=format, metadata=metadata, **kwargs)
