from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from pydantic import EmailStr
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.usuario import Usuario


class Rol(SQLModel, table=True):
    __tablename__='roles'

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=25)
    status: bool = Field(default=True)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory= datetime.now)

    usuarios: list[Usuario] = Relationship(back_populates='rol')