from datetime import datetime
from sqlmodel import SQLModel

class ArchivoCreate(SQLModel):
    nombre: str

class ArchivoRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    created_at: datetime

