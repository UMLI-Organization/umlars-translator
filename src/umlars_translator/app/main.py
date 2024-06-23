import os
from logging import Logger
from functools import partial

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi import Depends
from pymongo import MongoClient
from umlars_translator.app.adapters.repositories.uml_model_repository import UmlModelRepository
from umlars_translator.app.adapters.repositories.mongo_uml_model_repository import MongoDBUmlModelRepository
from umlars_translator.app.dtos.uml_model import UmlModel
from umlars_translator.app import config
from umlars_translator.logger import create_logger


app = FastAPI()
create_app_logger = partial(create_logger, level=config.LOG_LEVEL, logger_name=config.APP_LOGGER_NAME, logs_file=config.LOG_FILE)


def get_db_client(logger: Logger = Depends(create_app_logger)) -> MongoClient:
    try:
        connection_str = config.DB_CONN_STR
        return MongoClient(connection_str)
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to the database")        


def get_uml_model_repository(db_client: MongoClient = Depends(get_db_client)) -> UmlModelRepository:
    return MongoDBUmlModelRepository(db_client, config.DB_NAME, config.DB_COLLECTION_NAME)


@app.get("/uml-models/{model_id}")
def get_uml_model(model_id: str, model_repo: UmlModelRepository = Depends(get_uml_model_repository)):
    model = model_repo.get(model_id)
    if model is None:
        raise HTTPException(status_code=404, detail=f"Model with ID: {model_id} not found {x}")

    return model


@app.post("/uml-models")
def translate_uml_model(uml_model: UmlModel, model_repo: UmlModelRepository = Depends(get_uml_model_repository)):
    # TODO: translate
    return model_repo.save(uml_model)


def run_app(port: int = 8020) -> None:
    port = int(os.getenv("EXPOSE_ON_PORT", port))
    return uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    run_app()
