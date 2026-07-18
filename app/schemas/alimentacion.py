from datetime import datetime
from sqlmodel import SQLModel

class AlimentacionBase(SQLModel):
    nombre: str

class AlimentacionCreate(AlimentacionBase):
    pass 

class AlimentacionRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime
    