from sqlmodel import Session, select
from datetime import datetime

from app.utils.exceptions import NotFoundError, ConflictError

from app.models import Personal, Genero, Alimentacion,Ciudad,Eps, StatusPersonal
from app.schemas.personal import PersonalCreate, PersonalRead, PersonalUpdate

def create(datos:PersonalCreate, session: Session)-> PersonalRead:
    
    if not session.get(Genero,datos.genero_id):
        raise NotFoundError(f'El genero con el id {datos.genero_id} no existe')
    if not session.get(Alimentacion, datos.alimentacion_id):
        raise NotFoundError(f'La Alimentacion con el id {datos.alimentacion_id} no existe')
    if not session.get(Ciudad, datos.ciudad_id):
        raise NotFoundError(f'La ciudad con el id {datos.ciudad_id} no existe')
    if not session.get(Eps, datos.eps_id):
        raise NotFoundError(f'La eps con el id {datos.eps_id} no existe')
    if not session.get(StatusPersonal, datos.status_personal_id):
        raise NotFoundError(f'El status personal con el id {datos.status_personal_id} no existe') 
    
    new_person = Personal(**datos.model_dump())
    session.add(new_person)
    session.commit()
    session.refresh(new_person)
    return new_person

def get_all(session: Session) -> list[Personal]:
    return session.exec(select(Personal)).all()

def get_by_id(id:int, session:Session)->PersonalRead:
    return session.get(Personal,id)

def update(id:int, datos:PersonalUpdate, session: Session)->PersonalUpdate:
    registro= session.get(Personal,id)

    if not registro:
        return None

    # Validación si FK existen (Solo si fueron enviadas en la petición)

    if datos.genero_id is not None and not session.get(Genero, datos.genero_id):
        raise NotFoundError(f"El genero con el id {datos.genero_id} no existe")

    if datos.alimentacion_id is not None and not session.get(Alimentacion, datos.alimentacion_id):
        raise NotFoundError(f"La Alimentacion con el id {datos.alimentacion_id} no existe")

    if datos.ciudad_id is not None and not session.get(Ciudad, datos.ciudad_id):
        raise NotFoundError(f"La ciudad con el id {datos.ciudad_id} no existe")

    if datos.eps_id is not None and not session.get(Eps, datos.eps_id):
        raise NotFoundError(f"La eps con el id {datos.eps_id} no existe")

    if datos.status_personal_id is not None and not session.get(StatusPersonal, datos.status_personal_id):
        raise NotFoundError(f"El status personal con el id {datos.status_personal_id} no existe")

    datos_recibidos = datos.model_dump(exclude_unset=True)
    for key, value in datos_recibidos.items():
        setattr(registro, key, value)

    
    registro.updated_at = datetime.now()
    session.add(registro)
    session.commit()
    session.refresh(registro)    
    return registro

def delete(id: int, session:Session):
    registro = session.get(Personal, id)

    if not registro:
        return False
    
    session.delete(registro)
    session.commit()
    return True
