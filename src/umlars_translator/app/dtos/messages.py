from pydantic import BaseModel


class QueueMessage(BaseModel):
    ...


class ModelToTranslateMessage(QueueMessage):
    id: int | str
