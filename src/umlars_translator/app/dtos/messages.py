from typing import List, Union, Optional
from enum import IntEnum

from pydantic import BaseModel, ConfigDict

from umlars_translator.config import SupportedFormat


class ProcessStatusEnum(IntEnum):
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
    ids_of_edited_files: Optional[List[Union[int, str]]] = None
    ids_of_new_submitted_files: Optional[List[Union[int, str]]] = None
    ids_of_deleted_files: Optional[List[Union[int, str]]] = None


class TranslatedFileMessage(QueueMessage):
    id: str | int
    state: ProcessStatusEnum = ProcessStatusEnum.RUNNING
    message: Optional[str] = None
    process_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
