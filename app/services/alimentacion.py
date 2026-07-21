from sqlmodel import Session, select
from datetime import datetime
from app.models.alimentacion import Alimentacion
from app.schemas.alimentacion import AlimentacionCreate, AlimentacionRead

from app.utils.logger import logger
from app.utils.errors import NotFoundError, AlreadyExistsError, BussinesError, DatabaseError

from sqlalchemy.exc import IntegrityError

def create(session:Session, datos: AlimentacionCreate) -> Alimentacion:
    logger.debug(f'Creando alimentacion {datos.model_dump()}')
    alimentacion = Alimentacion(nombre= datos.nombre)
    session.add(alimentacion)

    try:
        session.commit()

    except IntegrityError as e:
        session.rollback()
        logger.warning(f'Intento de crear alimentacion duplicada: {datos.nombre}')
        raise AlreadyExistsError("Alimentacion", "nombre", datos.nombre)
    
    except Exception as e:
        session.rollback()
        logger.exception('Fallo inesperado al guardar Alimentacion')
        raise DatabaseError("No se pudo guardar el registro")

    session.refresh(alimentacion)
    logger.info(f'Alimentacion creada correctamente | id: {alimentacion.id} | nombre: {alimentacion.nombre}')
    return alimentacion

def get_all(session:Session) -> list[Alimentacion]:
    logger.debug(f'Buscando todas las alimentaciones')
    consulta = select(Alimentacion)
    
    try:
        resultados = session.exec(consulta).all()
    except Exception:
        logger.exception(f'No se pudo conectar a la BD')
        raise DatabaseError(f'No se pudo conectar a la BD')
    
    logger.info(f'Mostrando todas las alimentaciones')
    return resultados


def get_by_id(session:Session, id: int) -> Alimentacion | None:
    logger.debug(f'Buscando el id {id} en la tabla alimentaciones')
    consulta = session.get(Alimentacion, id)
    
    if not consulta:
        raise NotFoundError('Alimentacion', id)
    
    logger.info(f'Alimentacion: {consulta.nombre} encontrada con su id{consulta.id}')
    return consulta


def update(session: Session, id: int, datos: AlimentacionCreate) -> Alimentacion:
    logger.debug(f'Comenzando actualizacion del id {id} en la tabla alimentaciones')
    consulta = session.get(Alimentacion, id)
    if not consulta:
        raise NotFoundError('Alimentacion', id)

    consulta.nombre = datos.nombre
    consulta.updated_at = datetime.now()
    session.add(consulta)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        logger.warning(f'Intento de actualizar a nombre duplicado: {datos.nombre}')
        raise AlreadyExistsError("Alimentacion", "nombre", datos.nombre)
    except Exception:
        session.rollback()
        logger.exception('Fallo inesperado al actualizar Alimentacion')
        raise DatabaseError("No se pudo actualizar el registro")

    session.refresh(consulta)
    logger.info(f'Actualizacion exitosa en el id {consulta.id} ahora con nombre {consulta.nombre}')
    return consulta

def delete(session: Session, id: int) -> bool:
    logger.debug(f'Comenzando el borrado del id {id} en la tabla alimentaciones')
    consulta = session.get(Alimentacion, id)
    if not consulta:
        raise NotFoundError('Alimentacion', id)

    try:
        session.delete(consulta)
        session.commit()
    except IntegrityError:
        session.rollback()
        logger.warning(f'No se pudo eliminar Alimentacion id={id}, tiene registros relacionados')
        raise BussinesError("No se puede eliminar: hay personal asociado a esta alimentacion")
    except Exception:
        session.rollback()
        logger.exception('Fallo inesperado al eliminar Alimentacion')
        raise DatabaseError("No se pudo eliminar el registro")

    logger.info(f'Alimentacion eliminada | id: {id}')
    return True