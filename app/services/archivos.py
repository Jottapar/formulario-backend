from sqlmodel import Session, select
from datetime import datetime
import logging

from app.schemas.archivo import ArchivoCreate, ArchivoRead
from app.models.archivos import Archivos


logger = logging.getLogger(__name__)


def create(session: Session, datos:ArchivoCreate) -> ArchivoCreate:
    archivo= Archivos(nombre=datos.nombre)
    session.add(archivo)
    session.commit()
    session.refresh(archivo)
    logger.info(f'logger.info(f"ArchivoPersonal creado con id {archivo.id}") ')
    return archivo

def get_all(session: Session)-> ArchivoRead:
    consulta = select(Archivos)
    resultado = session.exec(consulta).all()
    return resultado


def get_by_id(id: int, session: Session)->ArchivoRead:
    return session.get(Archivos, id)


def update(id:int, datos:ArchivoCreate, session:Session)->ArchivoRead | None:
    archivo = session.get(Archivos, id)

    if archivo is None:
        return None
    
    archivo.nombre = datos.nombre
    archivo.updated_at = datetime.now()
    session.add(archivo)
    session.commit()
    session.refresh(archivo)
    return archivo

def delete(id: int, session: Session)-> bool:
    archivo = session.get(Archivos, id)

    if archivo is None:
        return False
    
    session.delete(archivo)
    session.commit()
    return True