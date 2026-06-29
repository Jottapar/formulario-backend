from datetime import datetime
from sqlmodel import SQLModel

class StatusPersonalCreate(SQLModel):
    nombre:str

class StatusPersonalRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime