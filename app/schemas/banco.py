from datetime import datetime
from sqlmodel import SQLModel

class BancoBase(SQLModel):
    nombre: str

class BancoCreate(BancoBase):
    pass

class BancoRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime 
    updated_at: datetime

