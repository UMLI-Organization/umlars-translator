import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from umlars_translator.app.repository import Base
from umlars_translator.app.main import app, get_db_session
from umlars_translator.app.repository import UmlModelRepository
from umlars_translator.app.repository import UmlModel


@pytest.fixture(scope="session")
def engine():
    _engine = create_engine(
        "sqlite://",
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(_engine)
    return _engine


@pytest.fixture
def session(engine):
    with engine.connect() as connection:
        transaction = connection.begin()
        session = Session(bind=connection)
        yield session
        session.close()
        transaction.rollback()


@pytest.fixture
def client(session):
    app.dependency_overrides[get_db_session] = lambda: session
    return TestClient(app)


@pytest.fixture
def model_repo(session) -> UmlModelRepository:
    return UmlModelRepository(session)


@pytest.fixture
def single_model_in_db(model_repo):
    model_repo.save(
        UmlModel(
            id="EXISTING",
            name="MODEL",
        )
    )