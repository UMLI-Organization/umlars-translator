import os
import logging
from contextlib import asynccontextmanager

from kink import di
import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from src.umlars_translator.app.utils.service_connector import ServiceConnector
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


async def start_consuming_messages() -> None:
    try:
        consumer = RabbitMQConsumer(config.MESSAGE_BROKER_QUEUE_NAME, config.MESSAGE_BROKER_HOST)
    except QueueUnavailableError as e:
        raise ServiceConnectionError("Failed to create a consumer for the message queue") from e
    return await consumer.start_consuming()


async def connect_services():
    try:
        repository_service_connector = ServiceConnector(config.REPOSITORY_API_URL, config.REPOSITORY_SERVICE_CREATE_JWT_ENDPOINT)
        await repository_service_connector.authenticate({"username": config.REPOSITORY_SERVICE_USER, "password": config.REPOSITORY_SERVICE_PASSWORD})
    except Exception as e:
        raise ServiceConnectionError("Failed to connect to the service") from e


@asynccontextmanager
async def lifespan_event_handler(app: FastAPI):
    try:
        try:
            await start_consuming_messages()
            await connect_services()
        except Exception as ex:
            import logging
            logging.error(f"Failed to start consuming messages: {ex}")
            print(f"Failed to start consuming messages: {ex}")
        yield
    except ServiceConnectionError as ex:
        raise ServiceConnectionError("Failed to start consuming messages") from ex


app = FastAPI(lifespan=lifespan_event_handler)


async def get_db_client(logger: logging.Logger = Depends(create_app_logger)) -> AsyncIOMotorClient:
    try:
        connection_str = config.DB_CONN_STR
        return AsyncIOMotorClient(connection_str)
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to the database")        


async def get_uml_model_repository(db_client: AsyncIOMotorClient = Depends(get_db_client)) -> UmlModelRepository:
    return MongoDBUmlModelRepository(db_client, config.DB_NAME, config.DB_COLLECTION_NAME)


@app.get("/uml-models/{model_id}")
async def get_uml_model(model_id: str, model_repo: UmlModelRepository = Depends(get_uml_model_repository)):
    model = await model_repo.get(model_id)
    if model is None:
        raise HTTPException(status_code=404, detail=f"Model with ID: {model_id} not found")
    return model


@app.post("/uml-models")
async def translate_uml_model(uml_model: UmlModel, model_repo: UmlModelRepository = Depends(get_uml_model_repository)):
    # TODO: translate
    await model_repo.save(uml_model)
    return {"status": "success"}


def run_app(port: int = 8080, host: str = "0.0.0.0", context: str = 'DEV', logger: logging.Logger = Depends(create_app_logger)) -> None:
    logger.error("\n\n\nStarted\n\n\n")

    port = int(os.getenv("EXPOSE_ON_PORT", port))
    if context == 'DEV':
        return uvicorn.run(app, host=host, port=port, reload=True)
    else:
        return uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_app()
