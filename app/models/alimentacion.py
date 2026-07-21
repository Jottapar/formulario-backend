from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .personal import Personal

class Alimentacion(SQLModel, table=True):
    __tablename__= "alimentaciones"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=15, unique=True)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    personal: list[Personal] = Relationship(back_populates="alimentacion")

