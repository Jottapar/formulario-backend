from sqlmodel import Session, select
from datetime import datetime
from app.models.banco import Banco
from app.schemas.banco import BancoCreate

from app.utils.logger import logger
from app.utils.errors import NotFoundError, DatabaseError




def create(session: Session, datos: BancoCreate) -> Banco:
    logger.debug(f'Creando un nuevo Banco con {datos.model_dump()}')
    banco = Banco(nombre=datos.nombre)
    
    try:
        session.add(banco)
        session.commit()

    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')
    
    session.refresh(banco)
    logger.info(f'Banco {banco.nombre} creado exitosamente')
    return banco


def get_all(session: Session) -> list[Banco]:
    logger.debug(f'Creando lista de todos los Bancos')

    try:
        consulta = session.exec(select(Banco)).all()

    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')
    
    return consulta

def get_by_id(session: Session, id: int) -> Banco:
    logger.debug(f'Buscando banco con id {id}')

    try:
        consulta = session.get(Banco, id)

    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')
    
    if not consulta:
        raise NotFoundError('Banco',id)

    return consulta

def update(session: Session, id: int, datos: BancoCreate) -> Banco:
    logger.debug(f'Actualizando banco con los siguientes datos {datos.model_dump()}')

    banco = session.get(Banco, id)
    
    if not banco:
        raise NotFoundError('Banco',id)
    
    banco.nombre = datos.nombre
    banco.updated_at = datetime.now()
    session.add(banco)

    try:
        session.commit()

    except Exception:
        logger.exception(f'Fallo conexion con base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')

    session.refresh(banco)
    return banco


def delete(session: Session, id: int) -> bool:
    logger.debug(f'Borrando banco con id {id}')
    banco = session.get(Banco, id)


    if not banco:
        raise NotFoundError('Banco', id)
    
    try:
        session.delete(banco)
        session.commit()

    except Exception:
        logger.exception(f'Fallo conexion con base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')
    
    return True