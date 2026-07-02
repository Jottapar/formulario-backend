from sqlmodel import Session, select
from datetime import datetime

from app.models.status_personal import StatusPersonal
from app.schemas.status_personal import StatusPersonalCreate, StatusPersonalRead

def create(datos: StatusPersonalCreate, session: Session) -> StatusPersonalRead:
    status= StatusPersonal(nombre=datos.nombre)
    session.add(status)
    session.commit()
    session.refresh(status)
    return status

def get_all(session: Session)->StatusPersonalRead:
    status = select(StatusPersonal)
    resultado = session.exec(status).all()
    return resultado

def get_by_id(id: int, session: Session)-> StatusPersonalRead:
    status = session.get(StatusPersonal, id)

    if status is None:
        return None
    
    return status

def update(id: int, datos: StatusPersonalCreate, session:Session)-> StatusPersonalRead:
    status = session.get(StatusPersonal, id)

    if status is None:
        return None
    
    status.nombre = datos.nombre
    status.updated_at = datetime.now()
    session.add(status)
    session.commit()
    session.refresh(status)
    return status

def delete(id: int, session:Session)-> bool:
    status = session.get(StatusPersonal, id)

    if status is None:
        return False
    
    session.delete(status)
    session.commit()
    return True
