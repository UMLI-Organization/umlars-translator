import os

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi import Depends

from umlars_translator.app.repository import UmlModelRepository


app = FastAPI()

_db = {
    "EXISTING": {"id": "EXISTING", "model": "MODEL"}
}


def get_uml_model_repository():
    return UmlModelRepository(_db)


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
