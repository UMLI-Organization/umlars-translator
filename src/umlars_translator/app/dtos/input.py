from typing import Optional, List

from pydantic import BaseModel
from src.umlars_translator.config import SupportedFormat


class UmlFile(BaseModel):
    id: str | int
    filename: str
    data: str
    format: Optional[SupportedFormat] = None

    class Config:
        from_attributes = True


class UmlModel(BaseModel):
    id: str | int
    source_files: List[UmlFile]

    class Config:
        from_attributes = True
