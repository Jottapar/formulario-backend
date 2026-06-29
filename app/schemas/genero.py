from datetime import datetime
from sqlmodel import SQLModel

class GeneroCreate(SQLModel):
    nombre: str

class GeneroRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime

