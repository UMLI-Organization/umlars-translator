from pydantic import BaseModel

from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy import select


class UmlModel(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


class Base(DeclarativeBase):
    """
    Base for ORM objects
    """


class _DbUmlModel(Base):
    __tablename__ = "UML_MODEL"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]


class UmlModelRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, model_id: str) -> UmlModel:
        orm_uml_model = self._session.execute(
            select(_DbUmlModel).where(_DbUmlModel.id == model_id)
        ).first()

        return UmlModel.model_validate(orm_uml_model[0]) if orm_uml_model is not None else None

    def save(self, uml_model: UmlModel) -> UmlModel:
        db_uml_model = self._session.get(_DbUmlModel, ident=uml_model.id) or _DbUmlModel(
            id=uml_model.id
        )

        db_uml_model.name = uml_model.name

        self._session.add(db_uml_model)
        self._session.flush()
        return self.get(uml_model.id)
