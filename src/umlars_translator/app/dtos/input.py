from typing import Optional, List

from pydantic import BaseModel

from src.umlars_translator.config import SupportedFormat
from src.umlars_translator.core.deserialization.data_source import DataSource


class UmlFileDTO(BaseModel):
    id: str | int
    filename: str
    data: str
    format: Optional[SupportedFormat] = None

    class Config:
        from_attributes = True

    def to_data_source(self) -> DataSource:
        return DataSource(self.data, format=self.format)


class UmlModelDTO(BaseModel):
    id: str | int
    source_files: List[UmlFileDTO]

    class Config:
        from_attributes = True

