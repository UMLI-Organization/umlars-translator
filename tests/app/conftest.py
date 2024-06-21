import pytest
from fastapi.testclient import TestClient

from umlars_translator.app.main import app, db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def single_model_in_db():
    db.clear()
    db["EXISTING"] = {"id": "EXISTING", "model": "MODEL"}

    yield

    db.clear()
