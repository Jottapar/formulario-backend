from datetime import datetime
from sqlmodel import SQLModel

class CiudadBase(SQLModel):
    nombre: str

class CiudadCreate(CiudadBase):
    pass

class CiudadRead(SQLModel):
    id: int 
    nombre: str
    created_at: datetime
    updated_at: datetime

