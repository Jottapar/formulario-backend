from sqlmodel import Session, select
from datetime import datetime
import logging

from sqlalchemy.exc import IntegrityError
from app.utils.errors import NotFoundError, AlreadyExistsError

from app.models.archivos_personal import ArchivosPersonal
from app.models.archivos import Archivos
from app.models.personal import Personal
from app.schemas.archivo_personal import ArchivoPersonalCreate, ArchivoPersonalRead,ArchivoPersonalUpdate


logger = logging.getLogger(__name__)


def create(datos:ArchivoPersonalCreate, session:Session)-> ArchivosPersonal:
    archivo = session.get(Archivos, datos.archivos_id)
    persona = session.get(Personal, datos.personal_id)

    if not archivo:
        raise NotFoundError(f'El archivo con id {datos.archivos_id} no existe')
    
    if not persona:
        raise NotFoundError(f'La persona con id {datos.personal_id} no existe')
    
    new_record = ArchivosPersonal(
        personal_id=datos.personal_id,
        archivos_id=datos.archivos_id,
        url=datos.url
    )
    
    session.add(new_record)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ConflictError("Esta persona ya tiene un archivo de este tipo")

    session.refresh(new_record)
    logger.info(f"ArchivoPersonal creado con id {new_record.id}")   # evento normal
    return new_record




def get_all(session: Session)-> list[ArchivosPersonal]:
    registros=select(ArchivosPersonal)
    resultado= session.exec(registros).all()
    return resultado

def get_by_personal_id(id:int, session:Session) -> list[ArchivosPersonal]:
    registros= select(ArchivosPersonal).where(ArchivosPersonal.personal_id == id)
    resultado= session.exec(registros).all()
    return resultado

def update_url(id:int, datos:ArchivoPersonalUpdate, session:Session) -> ArchivosPersonal:
    registro = session.get(ArchivosPersonal,id)

    if registro  is None:
        raise NotFoundError(f"Archivo personal con id {id} no existe")
    
    datos_registro = datos.model_dump(exclude_unset=True)   
    for campo, valor in datos_registro.items():
        setattr(registro, campo, valor)
    
    registro.updated_at = datetime.now()
    session.add(registro)
    session.commit()
    session.refresh(registro)
    return registro

def delete(id:int, session:Session)-> bool:
    registro = session.get(ArchivosPersonal,id)

    if registro is None:
        return False
    
    session.delete(registro)
    session.commit()
    return True




