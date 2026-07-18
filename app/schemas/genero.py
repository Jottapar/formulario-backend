from datetime import datetime
from sqlmodel import SQLModel

class GeneroBase(SQLModel):
    nombre: str

class GeneroCreate(GeneroBase):
    pass

class GeneroRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime

