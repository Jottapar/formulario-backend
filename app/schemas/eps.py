from datetime import datetime
from sqlmodel import SQLModel


class EpsBase(SQLModel):
    nombre: str

class EpsCreate(EpsBase):
    pass

class EpsRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime

