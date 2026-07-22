from sqlmodel import Session, select
from datetime import datetime

from app.models.eps import Eps
from app.schemas.eps import EpsCreate, EpsRead

from app.utils.logger import logger
from app.utils.errors import NotFoundError, DatabaseError

def create(datos:EpsCreate, session:Session) -> Eps:
    logger.debug(f'Creando Nuevo Eps con {datos.model_dump()}')
    eps = Eps(nombre=datos.nombre)
    session.add(eps)

    try:
        session.commit()
    except Exception:
        logger.exception(f'Fallo en la comunicacion con la base de datos')
        raise DatabaseError(f'Fallo en la comunicacion con la base de datos')
    
    session.refresh(eps)
    logger.info(f'Eps creada con exito')
    return eps

def get_all(session:Session)->list[Eps]:
    logger.debug(f'Creando listado con todas las eps')
    
    try:
        consulta = session.exec(select(Eps)).all()
    except Exception:
        logger.exception(f'Falla conexion con la base de datos')
        raise DatabaseError(f'Falla conexion con la base de datos')
    
    return consulta

def get_by_id(id: int, session: Session) -> Eps:
    logger.debug(f'Buscando eps por el id {id}')
    consulta = session.get(Eps, id)
    
    if not consulta:
        raise NotFoundError('Eps',id)
    
    return consulta

def update(id: int, datos:EpsCreate, session:Session)->Eps:
    logger.debug(f'Actualizando la Eps con id {id} con datos {datos.model_dump()}')
    eps=session.get(Eps, id)

    if not eps:
        raise NotFoundError('Eps', id)
    
    eps.nombre = datos.nombre
    eps.updated_at = datetime.now()
    session.add(eps)

    try:
        session.commit()
        session.refresh(eps)

    except Exception:
        logger.exception(f'Falla conexion con la Base de Datos')
        raise DatabaseError(f'Falla conexion con la Base de Datos')

    return eps

def delete(id: int, session:Session)->bool:
    logger.debug(f'Buscando eps con el id{id} para borrar')
    eps=session.get(Eps,id)
    
    if not eps:
        raise NotFoundError('Eps',id)
    
    try:
        session.delete(eps)
        session.commit()
    except Exception:
        logger.exception(f'Falla conexion con la base de datos')
        raise DatabaseError(f'Falla conexion con la base de datos')
    
    logger.info(f'Eps borrada exitosamente')
    return True