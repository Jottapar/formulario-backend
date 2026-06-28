from datetime import datetime
from sqlmodel import SQLModel

class BancoCreate(SQLModel):
    nombre: str

class BancoRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime 
    updated_at: datetime

