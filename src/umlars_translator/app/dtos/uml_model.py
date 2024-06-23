from pydantic import BaseModel


class UmlModel(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True
