from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import Optional

from umlars_translator.app.dtos.uml_model import UmlModel
from umlars_translator.app.adapters.repositories.uml_model_repository import UmlModelRepository


class MongoDBUmlModelRepository(UmlModelRepository):
    def __init__(self, db_client: MongoClient, dbname: str, collection_name: str):
        self._client = db_client
        self._db = self._client[dbname]
        self._collection = self._db[collection_name]

    def get(self, model_id: str) -> Optional[UmlModel]:
        db_model = self._collection.find_one({"_id": ObjectId(model_id)})
        return UmlModel(id=str(db_model["_id"]), name=db_model["name"]) if db_model else None

    def save(self, uml_model: UmlModel) -> UmlModel:
        self._collection.update_one(
            {"_id": ObjectId(uml_model.id)},
            {"$set": uml_model.model_dump()},
            upsert=True
        )
        return self.get(uml_model.id)
