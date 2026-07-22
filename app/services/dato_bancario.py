from sqlmodel import Session, select

from app.models.dato_bancario import DatoBancario
from app.models.banco import Banco
from app.models.tipo_cuenta_bancaria import TipoCuentaBancaria
from app.models.personal import Personal
from app.schemas.dato_bancario import DatoBancarioCreate


from app.utils.logger import logger
from app.utils.errors import NotFoundError, AlreadyExistsError, DatabaseError


def create(data: DatoBancarioCreate, session: Session) -> DatoBancario:
    logger.debug(f'Creando nueva relacion Dato bancario')

    banco = session.get(Banco, data.banco_id)
    if not banco:
        raise NotFoundError(f"El banco con id {data.banco_id} no existe")

    tipo = session.get(TipoCuentaBancaria, data.tipo_cuenta_id)
    if not tipo:
        raise NotFoundError(f"El tipo de cuenta con id {data.tipo_cuenta_id} no existe")
    
    personal = session.get(Personal,id)
    if not personal:
        raise NotFoundError('Personal',data.personal_id)

    cuenta = DatoBancario(
        num_cuenta=data.num_cuenta,
        banco_id=data.banco_id,
        tipo_cuenta_id=data.tipo_cuenta_id,
        personal_id=data.personal_id
    )
    session.add(cuenta)
    
    try:
        session.commit()
    except Exception as e:
        logger.exception(f'Fallo al guardar Alimentacion en la Base de DAtos')
        raise DatabaseError(f'No se pudo guardar el registro')

    session.refresh(cuenta)
    logger.info(f'Dato bancario creado existosamente {cuenta.model_dump()}')
    return cuenta


def get_all(session: Session) -> list[DatoBancario]:
    logger.debug(f'Creando lista de todos los datos_bancarios')
    consulta = session.exec(select(DatoBancario)).all()

    if not consulta:
        raise NotFoundError('Dato Bancario', id)
    
    logger.info(f'Lista de Dato bancario creada')
    return consulta


def get_by_id(id: int, session: Session) -> DatoBancario | None:
    logger.debug(f'Buscando datobancario con el id {id}')
    consulta =  session.get(DatoBancario, id)

    if not consulta:
        raise NotFoundError('DatoBancario',id)

    return consulta

def delete(id: int,session: Session) -> bool:
    logger.debug(f'Buscando DatoBancario con id {id} para borrar')
    cuenta = session.get(DatoBancario, id)
    
    if not cuenta:
        raise NotFoundError('Dato bancario',id)
    
    try:
        session.delete(cuenta)
        session.commit()

    except Exception:
        logger.exception(f'Fallo en la conexion a la base de datos')
        raise DatabaseError(f'Fallo en la conexion a la base de datos')

    return True