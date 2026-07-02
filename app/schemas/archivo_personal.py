from datetime import datetime
from sqlmodel import SQLModel

from app.schemas.personal import PersonalRead
from app.schemas.archivo import ArchivoRead

class ArchivoPersonalCreate(SQLModel):
    personal_id: int
    archivos_id: int
    url: str

class ArchivoPersonalRead(SQLModel):
    id: int
    personal: PersonalRead
    archivos: ArchivoRead
    url: str
    created_at: datetime
    updated_at: datetime

    

class ArchivoPersonalUpdate(SQLModel):
    url: str | None = None