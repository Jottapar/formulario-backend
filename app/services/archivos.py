from sqlmodel import Session, select
from datetime import datetime


from app.schemas.archivo import ArchivoCreate, ArchivoRead
from app.models.archivos import Archivo


from app.utils.logger import logger
from app.utils.errors import NotFoundError, DatabaseError


def create(session: Session, datos:ArchivoCreate) -> Archivo:
    logger.debug(f'Creando Nuevo archivo con {datos.model_dump()}')

    archivo= Archivo(nombre=datos.nombre)
    session.add(archivo)

    try:
        session.commit()
    except Exception:
        logger.exception(f'Fallo conexion con la Base de Datos')
        raise DatabaseError(f'Fallo comunicacion con Base de Datos')
    
    session.refresh(archivo)
    logger.info(f'Archivo creado con exito')
    return archivo

def get_all(session: Session)-> list[Archivo]:
    logger.debug(f'Creando lista de todos los archivos')

    try:
        consulta = session.exec(select(Archivo)).all()

    except Exception:
        logger.exception(f'Fallo conexion con la Base de Datos')
        raise DatabaseError(f'Fallo conexion con la Base de Datos')

    return consulta


def get_by_id(id: int, session: Session)->Archivo:
    logger.debug(f'Buscando archivo con id {id}')

    consulta = session.get(Archivo, id)

    if not consulta:
        raise NotFoundError("Archivo",id)
    
    return consulta


def update(id:int, datos:ArchivoCreate, session:Session)->Archivo:
    logger.debug(f'Inicializando actualizacion del archivo con {datos.model_dump()}')
    
    archivo = session.get(Archivo, id)

    if not archivo:
        raise NotFoundError('Archivo',id)
    
    archivo.nombre = datos.nombre
    archivo.updated_at = datetime.now()
    session.add(archivo)
    
    try:
        session.commit()

    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')
    
    session.refresh(archivo)
    return archivo

def delete(id: int, session: Session)-> bool:
    logger.debug(f'Buscando archivo con el id{id} para borrar')
    archivo = session.get(Archivo, id)

    if not archivo:
        raise NotFoundError('Archivo',id)
    
    try:
        session.delete(archivo)
        session.commit()

    except Exception:
        logger.exception(f'Fallo conexion con la base de datos')
        raise DatabaseError(f'Fallo conexion con la base de datos')
    
    return True