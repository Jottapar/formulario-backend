from sqlmodel import Session, select
from app.models.tipo_cuenta_bancaria import TipoCuentaBancaria
from app.schemas.tipo_cuenta_bancaria import TipoCuentaCreate
from datetime import datetime

from app.utils.logger import logger
from app.utils.errors import NotFoundError, DatabaseError

def create(session: Session, data: TipoCuentaCreate) -> TipoCuentaBancaria:
    logger.debug(f'Creando un nuevo tipo cuenta bancaria')
    tipo = TipoCuentaBancaria(nombre=data.nombre)
    session.add(tipo)

    try:
        session.commit()
        session.refresh(tipo)
    except Exception:
        logger.exception(f'Falla conexion con la base de datos')
        raise DatabaseError(f'Falla conexion con la base de datos')
    
    logger.info(f'TipoCuentaBancaria creada con exito')
    return tipo


def get_all(session: Session) -> list[TipoCuentaBancaria]:
    logger.debug(f'Creando lista de todo los TiposCuentaBancaria')
    
    try:
        consulta = session.exec(select(TipoCuentaBancaria)).all()
    except Exception:
        logger.exception(f'Falla conexion con base de datos')
        raise DatabaseError(f'Falla conexion con la base de datos')

    return consulta 


def get_(id: int, session: Session) -> TipoCuentaBancaria:
    logger.debug(f'Buscando TipoCuentaBancaria con id {id}')
    consulta = session.get(TipoCuentaBancaria, id)

    if not consulta:
        raise NotFoundError('TipoCuenta Bancaria',id)
    
    return consulta 


def update(id: int, data: TipoCuentaCreate, session: Session) -> TipoCuentaBancaria:
    logger.debug(f'Actualizando TipoCuentaBancaria con id {id} con datos {data.model_dump()}')
    tipo = session.get(TipoCuentaBancaria, id)

    if not tipo:
        raise NotFoundError('TipoCuentaBancaria', id)
    
    tipo.nombre = data.nombre
    tipo.updated_at = datetime.now()
    session.add(tipo)
    
    try:
        session.commit()
        session.refresh(tipo)
    except Exception:
        logger.exception(f'Falla conexion con la base de datos')
        raise DatabaseError(f'Falla conexion con la base de datos')
    
    logger.info(f'Actualizacion de TipoCuentaBancario existosa')
    return tipo


def delete(id: int, session: Session) -> bool:
    logger.debug(f'Buscando TipoCuentaBancario con id {id} para borrar')
    tipo = session.get(TipoCuentaBancaria, id)

    if not tipo:
        raise NotFoundError('TipoCuentaBancaria',id)
    
    try:
        session.delete(tipo)
        session.commit()
    except Exception:
        logger.exception(f'Falla conexion con la base de datos')
        raise DatabaseError(f'Falla conexion con la base de datos')
    
    logger.info(f'TipoCuentaBancaria borrada con exito')
    return True

