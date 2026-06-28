from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .dato_bancario import DatoBancario



class Banco(SQLModel, table=True):
    __tablename__ = "bancos"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=15)
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default_factory=datetime.now)

    datos_bancarios: list["DatoBancario"] = Relationship(back_populates="banco")