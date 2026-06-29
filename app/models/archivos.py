from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .archivos_personal import ArchivosPersonal

class Archivos(SQLModel, table=True):
    __tablename__= "archivos"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=25)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


    archivos_personal: list[ArchivosPersonal] = Relationship(back_populates="archivos")