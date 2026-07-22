from sqlmodel import Session, select
from datetime import datetime

from app.models.status_personal import StatusPersonal
from app.schemas.status_personal import StatusPersonalCreate, StatusPersonalRead

from app.utils.logger import logger
from app.utils.errors import NotFoundError, DatabaseError

def create(datos: StatusPersonalCreate, session: Session) -> StatusPersonal:
    logger.debug(f'Creando Status personal con {datos.model_dump()}')
    status= StatusPersonal(nombre=datos.nombre)
    session.add(status)

    try:
        session.commit()
        session.refresh(status)
    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')
    
    logger.info(f'Status Personal creado existosamente')
    return status

def get_all(session: Session)->StatusPersonal:
    logger.debug(f'Creando listado de Status de Personal')
    
    try:
        resultado = session.exec(select(StatusPersonal)).all()
    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')
    
    return resultado

def get_by_id(id: int, session: Session)-> StatusPersonal:
    logger.debug(f'Buscando statuspersonal con id {id}')
    status = session.get(StatusPersonal, id)

    if not status:
        raise NotFoundError("Status Personal", id)
    
    return status

def update(id: int, datos: StatusPersonalCreate, session:Session)-> StatusPersonal:
    logger.debug(f'Actualizando statusPersonal con id {id} con estos datos {datos}')

    status = session.get(StatusPersonal, id)

    if not status:
        raise NotFoundError('Status Personal', id)
    
    status.nombre = datos.nombre
    status.updated_at = datetime.now()
    session.add(status)

    try:
        session.commit()
        session.refresh(status)
    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')
    
    logger.info(f'StatusPersonal actualizado con existo')
    return status

def delete(id: int, session:Session)-> bool:
    logger.debug(f'Buscando statuspersonal con id {id} para borrar')
    status = session.get(StatusPersonal, id)

    if not status:
        raise NotFoundError('Status Personal', id)
    
    try:
        session.delete(status)
        session.commit()
    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')
    
    logger.info(f'StatusPersonal borrado con exito')
    return True
