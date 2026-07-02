from sqlmodel import Session, select
from datetime import datetime

from app.models.ciudad import Ciudad
from app.schemas.ciudad import CiudadCreate, CiudadRead

def create(datos: CiudadCreate, session: Session) -> Ciudad:
    ciudad = Ciudad(nombre=datos.nombre)
    session.add(ciudad)
    session.commit()
    session.refresh(ciudad)
    return ciudad

def get_all(session:Session) -> list[CiudadRead]:
    consulta = select(Ciudad)
    resultado = session.exec(consulta).all()
    return resultado

def get_by_id(id: int, session:Session) -> CiudadRead:
    return session.get(Ciudad, id)

def update(id: int, datos:CiudadCreate, session: Session) -> CiudadCreate:
    ciudad = session.get(Ciudad, id)

    if ciudad is None:
        return None
    
    ciudad.nombre = datos.nombre
    ciudad.updated_at = datetime.now()
    session.add(ciudad)
    session.commit()
    session.refresh(ciudad)
    return ciudad

def delete(id:int, session:Session) -> bool:
    ciudad = session.get(Ciudad, id)
    
    if not ciudad:
        return False
    
    session.delete(ciudad)
    session.commit()
    return True
