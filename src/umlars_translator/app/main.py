import os
import logging
from functools import partial
from contextlib import asynccontextmanager

from kink import di
import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi import Depends
from pymongo import MongoClient
from src.umlars_translator.app.adapters.repositories.uml_model_repository import UmlModelRepository
from src.umlars_translator.app.adapters.repositories.mongo_uml_model_repository import MongoDBUmlModelRepository
from src.umlars_translator.app.dtos.uml_model import UmlModel
from src.umlars_translator.app.adapters.message_brokers.rabbitmq_message_consumer import RabbitMQConsumer
from src.umlars_translator.app import config
from src.umlars_translator.app.exceptions import ServiceConnectionError, QueueUnavailableError


def create_app_logger():
    """
    This function provides consistent logger creation for the application.
    New logger for the application is created as a child of the main logger, 
    used in the core module.
    """
    app_logger = di[logging.Logger].getChild(config.APP_LOGGER_NAME)
    app_logger.setLevel(config.LOG_LEVEL)
    app_logger.addHandler(logging.FileHandler(config.LOG_FILE))
    return app_logger


def start_consuming_messages() -> None:
    try:
        consumer = RabbitMQConsumer(config.RABBITMQ_QUEUE_NAME, config.RABBITMQ_HOST)
    except QueueUnavailableError as e:
        raise ServiceConnectionError("Failed to create a consumer for the message queue") from e
    return consumer.start_consuming()


@asynccontextmanager
async def lifespan_event_handler(app: FastAPI):
    try:
        start_consuming_messages()
        yield
    except ServiceConnectionError as ex:
        raise ServiceConnectionError("Failed to start consuming messages") from ex


app = FastAPI(lifespan=lifespan_event_handler)


def get_db_client(logger: logging.Logger = Depends(create_app_logger)) -> MongoClient:
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
        raise HTTPException(status_code=404, detail=f"Model with ID: {model_id} not found")
    return model


@app.post("/uml-models")
def translate_uml_model(uml_model: UmlModel, model_repo: UmlModelRepository = Depends(get_uml_model_repository)):
    # TODO: translate
    return model_repo.save(uml_model)


def run_app(port: int = 8080, host: str = "0.0.0.0", context: str = 'DEV', logger: logging.Logger = Depends(create_app_logger)) -> None:
    logger.error("\n\n\nStarted\n\n\n")

    port = int(os.getenv("EXPOSE_ON_PORT", port))
    if context == 'DEV':
        return uvicorn.run(app, host=host, port=port, reload=True)
    else:
        return uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_app()
