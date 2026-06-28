from datetime import datetime
from sqlmodel import SQLModel


class TipoCuentaCreate(SQLModel):
    nombre: str


class TipoCuentaRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime