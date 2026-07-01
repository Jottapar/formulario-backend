from sqlmodel import Session, select
from datetime import datetime

from app.schemas.genero import GeneroRead, GeneroCreate
from app.models.genero import Genero


def create(datos: GeneroCreate, session: Session)-> GeneroCreate:
    genero=Genero(nombre=datos.nombre)
    session.add(genero)
    session.commit()
    session.refresh(genero)
    return genero

def get_all(session: Session)->list[GeneroRead]:
    genero = select(Genero)
    resultado = session.exec(genero).all()
    return resultado

def get_by_id(id: int,session:Session)->GeneroRead:
    return session.get(Genero, id)

def update(id:int, datos:GeneroCreate, session:Session) -> GeneroRead:
    genero = session.get(Genero, id)

    if genero is None:
        return None
    
    genero.nombre = datos.nombre
    genero.updated_at = datetime.now()
    session.add(genero)
    session.commit()
    session.refresh(genero)
    return genero

def delete(id: int, session:Session):
    genero = session.get(Genero, id)

    if genero is None:
        return None
    
    session.delete(genero)
    return True
