import pytest
from fastapi.testclient import TestClient

from umlars_translator.app.main import app, get_uml_model_repository
from umlars_translator.app.repository import UmlModelRepository


@pytest.fixture
def db():
    return {}


@pytest.fixture
def model_repo(db) -> UmlModelRepository:
    return UmlModelRepository(db)


@pytest.fixture
def client(model_repo):
    app.dependency_overrides[get_uml_model_repository] = lambda: model_repo
    return TestClient(app)


@pytest.fixture
def single_model_in_db(db):
    db.clear()
    db["EXISTING"] = {"id": "EXISTING", "model": "MODEL"}

    yield

    db.clear()
