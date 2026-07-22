from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from typing import TYPE_CHECKING



if TYPE_CHECKING:
     from app.models.genero import Genero
     from app.models.alimentacion import Alimentacion
     from app.models.ciudad import Ciudad
     from app.models.eps import Eps
     from app.models.status_personal import StatusPersonal
     from app.models.dato_bancario import DatoBancario
     from app.models.archivos_personal import ArchivosPersonal

class Personal(SQLModel, table=True):
    __tablename__= "personal"

    id: int | None = Field(default=None, primary_key=True)
    tipo_doc: str = Field(max_length=3)
    num_doc: str = Field(max_length=10)
    primer_nombre: str
    segundo_nombre: str | None
    primer_apellido: str
    segundo_apellido: str | None
    telefono: str
    fecha_nacimiento: date
    correo: EmailStr
    direccion: str = Field(max_length=100)
    nombre_emergencia: str
    telefono_emergencia: str
    estatura: int
    talla_camiseta: str
    talla_pantalon: str
    talla_zapatos: str
    alergias: str
    nivel_ingles: str

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    genero_id: int = Field(foreign_key="generos.id")
    alimentacion_id: int = Field(foreign_key="alimentaciones.id")
    ciudad_id: int = Field(foreign_key="ciudades.id")
    eps_id: int = Field(foreign_key="eps.id")
    status_personal_id: int = Field(foreign_key="status_personal.id")

    genero: "Genero" = Relationship(back_populates="personal")
    datos_bancarios: list[DatoBancario] = Relationship(back_populates="personal")
    ciudad: "Ciudad" = Relationship(back_populates="personal")
    eps: "Eps" = Relationship(back_populates="personal")
    alimentacion: "Alimentacion" = Relationship(back_populates="personal")
    status_personal: "StatusPersonal" = Relationship(back_populates="personal")
    archivos_personal: list[ArchivosPersonal] = Relationship(back_populates="personal")

