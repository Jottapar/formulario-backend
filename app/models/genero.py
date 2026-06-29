from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.personal import Personal


class Genero (SQLModel, table=True):
    __tablename__= "generos"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=15)

    created_at: datetime = Field(default_factory= datetime.now)
    updated_at: datetime = Field(default_factory= datetime.now)

    personal: list[Personal] = Relationship(back_populates="genero")
