from datetime import datetime
from sqlmodel import SQLModel


class StatusPersonalBase(SQLModel):
    nombre:str

class StatusPersonalCreate(StatusPersonalBase):
    pass

class StatusPersonalRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime