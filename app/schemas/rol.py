from sqlmodel import SQLModel
from datetime import datetime

from app.models.rol import Rol

class RolBase(SQLModel):
    nombre: str
    status: bool

class RolCreate(RolBase):
    pass 

class RolRead(SQLModel):
    id: int
    nombre: str
    status: bool
    created_at: datetime
    updated_at: datetime
