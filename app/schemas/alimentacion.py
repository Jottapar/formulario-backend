from datetime import datetime
from sqlmodel import SQLModel

class AlimentacionCreate(SQLModel):
    nombre: str 

class AlimentacionRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime
    