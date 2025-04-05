from typing import Optional

from pymongo import MongoClient
from pymongo.results import UpdateResult

from umlars_translator.app.dtos.uml_model import UmlModel
from umlars_translator.app.adapters.repositories.uml_model_repository import UmlModelRepository


class MongoDBUmlModelRepository(UmlModelRepository):
    def __init__(self, db_client: MongoClient, dbname: str, collection_name: str):
        self._client = db_client
        self._db = self._client[dbname]
        self._collection = self._db[collection_name]

    async def get(self, model_id: str) -> Optional[UmlModel]:
        db_model = await self._collection.find_one({"_id": str(model_id)})
        return UmlModel.from_mongo(db_model) if db_model else None
            
    async def save(self, uml_model: UmlModel) -> UpdateResult:
        result = await self._collection.update_one(
            {"_id": str(uml_model.id)},
            {"$set": uml_model.model_dump()},
            upsert=True
        )
        return result
