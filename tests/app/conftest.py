import pytest
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from bson.objectid import ObjectId
from pymongo import MongoClient

from src.umlars_translator.app.main import app, get_db_client
from src.umlars_translator.app.adapters.repositories.mongo_uml_model_repository import MongoDBUmlModelRepository


@pytest.fixture
def existing_model_id_str_value():
    EXISTING_MODEL_ID_VALUE = "123456789123123456789123"
    return EXISTING_MODEL_ID_VALUE


@pytest.fixture
def not_existing_id_str_value():
    NOT_EXISTING_MODEL_ID_VALUE = "123456789123123456789012"
    return NOT_EXISTING_MODEL_ID_VALUE


@pytest.fixture
def existing_model_name():
    EXISTING_MODEL_NAME_VALUE = "MODEL"
    return EXISTING_MODEL_NAME_VALUE


@pytest.fixture
def db_client():
    mock_client = MagicMock(spec=MongoClient)
    db_mock = mock_client.__getitem__.return_value 
    collection_mock = db_mock.__getitem__.return_value
    collection_mock.find_one.return_value = None
    return mock_client


@pytest.fixture
def not_existing_model_id():
    return ObjectId()


@pytest.fixture
def client(db_client):
    app.dependency_overrides[get_db_client] = lambda: db_client
    return TestClient(app)


@pytest.fixture
def model_repo(db_client) -> MongoDBUmlModelRepository:
    model_repo = MongoDBUmlModelRepository(db_client, "test_db", "test_collection")
    return model_repo


@pytest.fixture
def single_model_in_db(model_repo, existing_model_id_str_value, existing_model_name):
    model_repo._collection.find_one.return_value = {"_id": ObjectId(existing_model_id_str_value), "name": existing_model_name}
    yield
    model_repo._collection.find_one.return_value = None
