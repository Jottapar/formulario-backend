from sqlmodel import Session, select
from datetime import datetime

from app.models.eps import Eps
from app.schemas.eps import EpsCreate, EpsRead

def create(datos:EpsCreate, session:Session) -> EpsCreate:
    eps = Eps(nombre=datos.nombre)
    session.add(eps)
    session.commit()
    session.refresh(eps)
    return eps

def get_all(session:Session)->list[EpsRead]:
    eps = select(Eps)
    resultado = session.exec(eps).all()
    return resultado

def get_by_id(id: int, session: Session) -> EpsRead:
    return session.get(Eps, id)

def update(id: int, datos:EpsCreate, session:Session)->EpsRead:
    eps=session.get(Eps, id)

    if eps is None:
        return None
    
    eps.nombre = datos.nombre
    eps.updated_at = datetime.now()
    session.add(eps)
    session.commit()
    session.refresh(eps)
    return eps

def delete(id: int, session:Session)->bool:
    eps=session.get(Eps,id)


    if not eps:
        return False
    
    session.delete(eps)
    session.commit()
    return True