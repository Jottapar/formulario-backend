from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .banco import Banco
    from .tipo_cuenta_bancaria import TipoCuentaBancaria
    from .personal import Personal


class DatoBancario(SQLModel, table=True):
    __tablename__ = "datos_bancarios"

    id: int | None = Field(default=None, primary_key=True)
    num_cuenta: str = Field(index=True)

    banco_id: int = Field(foreign_key="bancos.id")
    tipo_cuenta_id: int = Field(foreign_key="tipos_cuentas_bancarias.id")
    personal_id: int = Field(foreign_key="personal.id") 

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # --- Navegación Python (lado "MUCHOS": van SIN lista, es un solo objeto) ---
    banco: "Banco" = Relationship(back_populates="datos_bancarios")
    tipo_cuenta: "TipoCuentaBancaria" = Relationship(back_populates="datos_bancarios")
    personal: "Personal" = Relationship(back_populates="datos_bancarios")