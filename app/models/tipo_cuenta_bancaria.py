from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .dato_bancario import DatoBancario

class TipoCuentaBancaria(SQLModel, table=True):
    __tablename__ = "tipos_cuentas_bancarias"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50)
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default=None)

    datos_bancarios: list["DatoBancario"] = Relationship(back_populates="tipo_cuenta")