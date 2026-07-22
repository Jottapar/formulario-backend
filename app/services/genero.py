from sqlmodel import Session, select
from datetime import datetime

from app.schemas.genero import GeneroRead, GeneroCreate
from app.models.genero import Genero

from app.utils.logger import logger
from app.utils.errors import NotFoundError, DatabaseError

def create(datos: GeneroCreate, session: Session)-> Genero:
    logger.debug(f'Creando Genero')
    genero=Genero(nombre=datos.nombre)
    session.add(genero)

    try:
        session.commit()
        session.refresh(genero)
    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')
    
    logger.info(f'Genero creado con exito')
    return genero

def get_all(session: Session)->list[Genero]:
    logger.debug(f'Creando listado de Generos')
    consulta = session.exec(select(Genero)).all()
    return consulta

def get_by_id(id: int,session:Session)->Genero:
    logger.debug(f'Buscando genero con id {id}')
    consulta = session.get(Genero, id)

    if not consulta:
        raise NotFoundError('Genero',id)
    
    return consulta

def update(id:int, datos:GeneroCreate, session:Session) -> GeneroRead:
    logger.debug(f'Actualizando Genero con el id{id} y estos datos {datos.model_dump()}')
    genero = session.get(Genero, id)

    if not genero:
        raise NotFoundError('Genero', id)
    
    genero.nombre = datos.nombre
    genero.updated_at = datetime.now()
    session.add(genero)

    try:
        session.commit()
        session.refresh(genero)

    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')

    logger.info(f'Genero con id {id} actualizado con exito')
    return genero

def delete(id: int, session:Session):
    logger.debug(f'Buscando genero con id {id} para borrar')
    genero = session.get(Genero, id)

    if not genero:
        raise NotFoundError('Genero',id)
    
    try:
        session.delete(genero)
        session.commit()
    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')

    logger.info(f'Genero Borrado con exito')
    return True
