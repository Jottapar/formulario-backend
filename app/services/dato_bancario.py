from sqlmodel import Session, select

from app.models.dato_bancario import DatoBancario
from app.models.banco import Banco
from app.models.tipo_cuenta_bancaria import TipoCuentaBancaria
from app.schemas.dato_bancario import DatoBancarioCreate


from app.utils.logger import logger
from app.utils.errors import NotFoundError, AlreadyExistsError, DatabaseError


def crear(session: Session, data: DatoBancarioCreate) -> DatoBancario:
    logger.debug(f'Creando nueva relacion Dato bancario')

    banco = session.get(Banco, data.banco_id)
    if not banco:
        raise NotFoundError(f"El banco con id {data.banco_id} no existe")

    tipo = session.get(TipoCuentaBancaria, data.tipo_cuenta_id)
    if not tipo:
        raise NotFoundError(f"El tipo de cuenta con id {data.tipo_cuenta_id} no existe")

    cuenta = DatoBancario(
        num_cuenta=data.num_cuenta,
        banco_id=data.banco_id,
        tipo_cuenta_id=data.tipo_cuenta_id,
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


def listar(session: Session) -> list[DatoBancario]:

    return session.exec(select(DatoBancario)).all()


def obtener(session: Session, cuenta_id: int) -> DatoBancario | None:
    return session.get(DatoBancario, cuenta_id)


def eliminar(session: Session, cuenta_id: int) -> bool:
    cuenta = session.get(DatoBancario, cuenta_id)
    if not cuenta:
        return False
    session.delete(cuenta)
    session.commit()
    return True