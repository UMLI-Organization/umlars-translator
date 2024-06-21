from typing import Optional
from pydantic import BaseModel


class UmlModel(BaseModel):
    id: str
    metadata: dict
    diagrams: Optional[list]
    elements: Optional[dict]


class UmlModelRepository:
    def __init__(self, db: dict) -> None:
        self._db: dict = db

    def get(self, model_id: str) -> UmlModel:
        return self._db.get(model_id)

    def save(self, model: UmlModel) -> None:
        self._db[model.id] = model
        return self.get(model.id)

    def clear(self) -> None:
        self._db.clear()
