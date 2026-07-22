from sqlmodel import Session, select
from datetime import datetime

from app.models.ciudad import Ciudad
from app.schemas.ciudad import CiudadCreate, CiudadRead

from app.utils.logger import logger
from app.utils.errors import NotFoundError,AlreadyExistsError,DatabaseError, BussinesError

def create(datos: CiudadCreate, session: Session) -> Ciudad:
    logger.debug(f'Creando Ciudad nueva con {datos.model_dump()}')
    ciudad = Ciudad(nombre=datos.nombre)
    session.add(ciudad)

    try:
        session.commit()
    
    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')
    
    session.refresh(ciudad)
    logger.info(f'Creacion Exitosa de la ciudad {ciudad.nombre}')

    return ciudad

def get_all(session:Session) -> list[Ciudad]:
    logger.debug(f'Creanod lista de todas las Ciudades')
    
    try:
        resultado = session.exec(select(Ciudad)).all()

    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')
    
    return resultado

def get_by_id(id: int, session:Session) -> Ciudad:
    logger.debug(f'Buscando ciudad con id {id}')

    consulta = session.get(Ciudad, id)

    if not consulta:
        raise NotFoundError('Ciudad',id)

    return consulta

def update(id: int, datos:CiudadCreate, session: Session) -> Ciudad:
    logger.debug(f'Actualizando Ciudad con {datos.model_dump()}')
    ciudad = session.get(Ciudad, id)

    if not ciudad:
        raise NotFoundError('Ciudad',id)
    
    ciudad.nombre = datos.nombre
    ciudad.updated_at = datetime.now()
    session.add(ciudad)

    try:
        session.commit()
        session.refresh(ciudad)
    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')
    return ciudad

def delete(id:int, session:Session) -> bool:
    logger.debug(f'Borrando Ciudad con el id {id}')

    ciudad = session.get(Ciudad, id)
    
    if not ciudad:
        raise NotFoundError('Ciudad',id)
    
    try:
        session.delete(ciudad)
        session.commit()
    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')
    
    return True
