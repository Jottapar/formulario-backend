from sqlmodel import Session, select
from datetime import datetime


from sqlalchemy.exc import IntegrityError
from app.utils.errors import NotFoundError, AlreadyExistsError, DatabaseError

from app.models.archivos_personal import ArchivosPersonal
from app.models.archivos import Archivo
from app.models.personal import Personal
from app.schemas.archivo_personal import ArchivoPersonalCreate,ArchivoPersonalUpdate

from app.utils.logger import logger

def create(datos:ArchivoPersonalCreate, session:Session)-> ArchivosPersonal:
    logger.debug(f'Creando archivos_personal de la personal {datos.model_dump()}')

    archivo = session.get(Archivo, datos.archivos_id)
    persona = session.get(Personal, datos.personal_id)

    if not archivo:
        raise NotFoundError('Archivo',datos.archivos_id)
    
    if not persona:
        raise NotFoundError('Personal',datos.personal_id)
    
    new_record = ArchivosPersonal(
        personal_id=datos.personal_id,
        archivos_id=datos.archivos_id,
        url=datos.url
    )
    
    session.add(new_record)

    try:
        session.commit()
        
    except IntegrityError:
        session.rollback()
        logger.warning(f'Ya existe un archivo {datos.archivos_id} asociado a personal {datos.personal_id}')
        raise AlreadyExistsError('ArchivosPersonal', 'personal_id + archivos_id', f'{datos.personal_id}-{datos.archivos_id}')
    except Exception:
        session.rollback()
        logger.exception('Fallo inesperado al crear ArchivosPersonal')
        raise DatabaseError('No se pudo guardar el registro')

    session.refresh(new_record)
    logger.info(f"ArchivoPersonal creado con id {new_record.id}")
    return new_record


def get_all(session: Session)-> list[ArchivosPersonal]:
    logger.debug(f'Buscando todos los archivos de personal')
    
    try:
        registros=select(ArchivosPersonal)
        resultado= session.exec(registros).all()
    except Exception:
        logger.exception('Fallo al conectarse a la base de datos')
        raise DatabaseError('Fallo al conectarse a la base de datos')
    
    logger.info(f'Listado de archivo_personal creado')
    return resultado


def get_by_personal_id(id: int, session: Session) -> list[ArchivosPersonal]:
    logger.debug(f'Buscando Archivos asociados a la persona con id {id}')

    persona = session.get(Personal, id)
    if not persona:
        raise NotFoundError('Personal', id)

    try:
        registros = select(ArchivosPersonal).where(ArchivosPersonal.personal_id == id)
        resultado = session.exec(registros).all()
    except Exception:
        logger.exception('Fallo al conectarse a la base de datos')
        raise DatabaseError('Fallo al conectarse a la base de datos')

    logger.info(f'{len(resultado)} archivo(s) encontrados para persona id {id}')
    return resultado


def update_url(id:int, datos:ArchivoPersonalUpdate, session:Session) -> ArchivosPersonal:
    logger.debug(f'Actualizar id con los siguientes datos {datos.model_dump()}')

    registro = session.get(ArchivosPersonal,id)

    if not registro:
        raise NotFoundError('ArchivosPersonal', id)

    datos_registro = datos.model_dump(exclude_unset=True)   
    for campo, valor in datos_registro.items():
        setattr(registro, campo, valor)
    
    registro.updated_at = datetime.now()
    session.add(registro)
    
    try:
        session.commit()
    
    except Exception:
        logger.exception(f'No se pudo conectar a la base de datos')
        raise DatabaseError('Fallo al conectarse a la base de datos')
    
    session.refresh(registro)

    logger.info(f'Actualizacion de archivos del persona con id {id} completado')
    return registro


def delete(id: int, session: Session) -> bool:
    logger.debug(f'Buscando id {id} de archivo_personal para borrarlo')

    registro = session.get(ArchivosPersonal, id)
    if not registro:
        raise NotFoundError('ArchivosPersonal', id)

    try:
        session.delete(registro)
        session.commit()
    except Exception:
        session.rollback()
        logger.exception('Fallo en conexión con base de datos')
        raise DatabaseError('Fallo en conexión con base de datos')

    logger.info(f'ArchivoPersonal id {id} eliminado')
    return True




