from typing import List, Union, Optional
from enum import Enum

from pydantic import BaseModel, ConfigDict

from src.umlars_translator.config import SupportedFormat


class ProcessStatusEnum(Enum):
    """Enum representing the status of a process."""
    QUEUED = 10
    RUNNING = 20
    FINISHED = 30
    PARTIAL_SUCCESS = 40
    FAILED = 50


class QueueMessage(BaseModel):
    ...


class ModelToTranslateMessage(QueueMessage):
    id: Union[int, str]
    ids_of_source_files: List[Union[int, str]]
    ids_of_edited_files: List[Union[int, str]]
    ids_of_new_submitted_files: List[Union[int, str]]
    ids_of_deleted_files: List[Union[int, str]]


class TranslatedFileMessage(QueueMessage):
    id: str | int
    state: ProcessStatusEnum = ProcessStatusEnum.RUNNING
    message: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
