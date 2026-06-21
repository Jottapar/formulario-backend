from datetime import datetime
from sqlmodel import SQLModel


# Lo que el cliente ENVÍA para crear un banco
class BancoCreate(SQLModel):
    nombre: str


# Lo que el servidor DEVUELVE al cliente
class BancoRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime | None
    updated_at: datetime | None