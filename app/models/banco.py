from datetime import datetime
from sqlmodel import SQLModel, Field


class Banco(SQLModel, table=True):
    __tablename__ = "bancos"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=15)
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default=None)