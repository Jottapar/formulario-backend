from datetime import datetime
from sqlmodel import SQLModel


class TipoCuentaBase(SQLModel):
    nombre: str

class TipoCuentaCreate(TipoCuentaBase):
    pass


class TipoCuentaRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime