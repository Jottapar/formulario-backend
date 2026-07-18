from sqlmodel import SQLModel
from datetime import datetime
from pydantic import EmailStr
from app.models.usuario import Usuario

class UsuarioBase(SQLModel):
    nombre: str 
    apellido: str 
    correo: EmailStr
    password: str 
    rol_id: int


class UsuarioCreate(UsuarioBase):
    pass 

class UsuarioRead(SQLModel):
    id: int
    nombre: str 
    apellido: str 
    correo: EmailStr
    rol_id: int

    created_at: datetime
    updated_at: datetime
