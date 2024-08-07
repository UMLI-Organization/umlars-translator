from typing import List, Union

from pydantic import BaseModel


class QueueMessage(BaseModel):
    ...


class ModelToTranslateMessage(QueueMessage):
    id: Union[int, str]
    ids_of_source_files: List[Union[int, str]]
    ids_of_edited_files: List[Union[int, str]]
    ids_of_new_submitted_files: List[Union[int, str]]
    ids_of_deleted_files: List[Union[int, str]]
