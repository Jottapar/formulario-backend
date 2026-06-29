from datetime import datetime, date
from sqlmodel import SQLModel, Field
from pydantic import EmailStr

from .genero import GeneroRead
from .alimentacion import AlimentacionRead
from .ciudad import CiudadRead
from .eps import EpsRead
from .status_personal import StatusPersonalRead
from .dato_bancario import DatoBancarioRead


class PersonalCreate(SQLModel):
    tipo_doc: str = Field(max_length=3)
    num_doc: str = Field(max_length=10)
    primer_nombre: str
    segundo_nombre: str | None
    primer_apellido: str
    segundo_apelido: str | None
    telefono: str
    fecha_nacimiento: date
    correo: EmailStr
    direccion: str = Field(max_length=100)
    nombre_emergencia: str = Field(max_length=100)
    telefono_emergencia: str = Field(max_length=13)
    estatura: int
    talla_camiseta: str
    talla_pantalon: str
    talla_zapatos: str
    alergias: str
    nivel_ingles: str
    
    
    genero_id: int
    alimentacion_id: int
    ciudad_id: int
    eps_id: int
    status_personal_id: int
    archivos_personal_id: int

class PersonalRead(SQLModel):
    id: int
    tipo_doc: str
    num_doc: str
    primer_nombre: str
    segundo_nombre: str | None
    primer_apellido: str
    segundo_apellido: str | None
    telefono: str
    fecha_nacimiento: date
    correo: EmailStr
    direccion: str
    nombre_emergencia: str
    telefono_emergencia: str
    estatura: int
    talla_camiseta: str
    talla_pantalon: str
    talla_zapatos: str
    alergias: str
    nivel_ingles: str

    created_at: datetime
    updated_at: datetime

    genero: GeneroRead
    alimentacion: AlimentacionRead
    ciudad: CiudadRead
    eps: EpsRead
    status_personal: StatusPersonalRead
    datos_bancarios: list[DatoBancarioRead]


