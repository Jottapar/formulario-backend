from datetime import datetime
from sqlmodel import SQLModel

class EpsCreate(SQLModel):
    nombre: str

class EpsRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime

