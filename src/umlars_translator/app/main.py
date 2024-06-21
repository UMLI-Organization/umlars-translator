import os

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from umlars_translator.app.repository import UmlModelRepository
from umlars_translator.app.repository import Base


app = FastAPI()
engine = create_engine("sqlite:///uml_model.db")
Base.metadata.create_all(engine)


def get_db_session():
    sesion = Session(engine)
    with sesion.begin() as session:
        yield session


def get_uml_model_repository(session: Session = Depends(get_db_session)):
    return UmlModelRepository(session)


@app.get("/uml-models/{model_id}")
def get_uml_model(model_id: str, model_repo: UmlModelRepository = Depends(get_uml_model_repository)):
    model = model_repo.get(model_id)
    if model is None:
        raise HTTPException(status_code=404, detail=f"Model with ID: {model_id} not found")
    
    return model



def run_app(port: int = 8020) -> None:
    return uvicorn.run(app, host="0.0.0.0", port=os.getenv("EXPOSE_ON_PORT", port))


if __name__ == "__main__":
    run_app()
