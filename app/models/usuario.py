from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from pydantic import EmailStr
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.rol import Rol


class Usuario(SQLModel,table= True):
    __tablename__='usuarios'

    id: int| None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=25)
    apellido: str = Field(max_length=25)
    correo: EmailStr = Field(max_length=100)
    password: str
    rol_id: int = Field(foreign_key= 'roles.id')

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory= datetime.now)

    rol: 'Rol' = Relationship(back_populates='usuarios')