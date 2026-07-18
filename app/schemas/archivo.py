from datetime import datetime
from sqlmodel import SQLModel

class ArchivoBase(SQLModel):
    nombre: str

class ArchivoCreate(ArchivoBase):
    pass

class ArchivoRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    created_at: datetime

