from datetime import datetime
from sqlmodel import SQLModel

class CiudadCreate(SQLModel):
    nombre: str 

class CiudadRead(SQLModel):
    id: int 
    nombre: str
    created_at: datetime
    updated_at: datetime

