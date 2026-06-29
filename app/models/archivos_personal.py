from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .personal import Personal
    from .archivos import Archivos

class ArchivosPersonal(SQLModel, table=True):
    __tablename__= "archivos_personal"
    __table_args__= (
        UniqueConstraint("personal_id","archivos_id", name="uq_persona_tipo"),
    )

    id: int | None = Field(default=None, primary_key=True)
    personal_id: int = Field(foreign_key="personal.id")
    archivos_id: int = Field(foreign_key="archivos.id")
    url: str

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    personal: "Personal" = Relationship(back_populates="archivos_personal")
    archivos: "Archivos" = Relationship(back_populates="archivos_personal")