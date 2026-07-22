from sqlmodel import Session, select
from datetime import datetime

from app.utils.errors import NotFoundError

from app.models import Personal, Genero, Alimentacion,Ciudad,Eps, StatusPersonal
from app.schemas.personal import PersonalCreate, PersonalRead, PersonalUpdate

from app.utils.logger import logger
from app.utils.errors import NotFoundError, DatabaseError

def create(datos:PersonalCreate, session: Session)-> Personal:
    logger.debug(f'Creando Personal Nuevo')    
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

    try:
        session.commit()
        session.refresh(new_person)
    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')
    
    logger.info(f'Personal creado correctamente')
    return new_person

def get_all(session: Session) -> list[Personal]:
    logger.debug(f'Creando listado de todo el personal')
    
    try:
        consulta = session.exec(select(Personal)).all()
    except Exception:
        logger.exception(f'Fallo conexxion con la base de datos')
        raise DatabaseError(f'Fallo conexxion con la base de datos')

    return consulta

def get_by_id(id:int, session:Session)->Personal:
    logger.debug(f'Buscando personal con id {id}')
    consulta = session.get(Personal,id)

    if not consulta:
        raise NotFoundError('Personal',id)
  
    return consulta

def update(id:int, datos:PersonalUpdate, session: Session)->Personal:
    logger.debug(f'Actualizando personal con id {id}')
    
    registro= session.get(Personal,id)

    if not registro:
        raise NotFoundError('Personal',id)

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
    
    try:
        session.commit()
        session.refresh(registro)
    except Exception:
        logger.exception(f'Falla conexion con la base de datos')
        raise DatabaseError(f'Falla conexion con la base de datos')

    logger.info(f'Personal actualizado con exito')
    return registro

def delete(id: int, session:Session):
    logger.debug(f'Buscando Personal con id {id} para borrar')
    registro = session.get(Personal, id)

    if not registro:
        raise NotFoundError('Personal', id)
    
    try:
        session.delete(registro)
        session.commit()
    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')

    logger.info(f'Personal borrado con exito')
    return True
