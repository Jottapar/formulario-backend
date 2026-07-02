from sqlmodel import Session, select

from app.utils.exceptions import NotFoundError, ConflictError

from app.models.dato_bancario import DatoBancario
from app.models.banco import Banco
from app.models.tipo_cuenta_bancaria import TipoCuentaBancaria
from app.schemas.dato_bancario import DatoBancarioCreate


def crear(session: Session, data: DatoBancarioCreate) -> DatoBancario:
    # --- VALIDACIÓN DE INTEGRIDAD REFERENCIAL (lo nuevo) ---
    # Antes de insertar, confirmo que las dos FK apunten a algo real.
    banco = session.get(Banco, data.banco_id)
    if not banco:
        raise NotFoundError(f"El banco con id {data.banco_id} no existe")

    tipo = session.get(TipoCuentaBancaria, data.tipo_cuenta_id)
    if not tipo:
        raise NotFoundError(f"El tipo de cuenta con id {data.tipo_cuenta_id} no existe")

    # Si llegué aquí, las dos FK son válidas → inserto con seguridad.
    cuenta = DatoBancario(
        num_cuenta=data.num_cuenta,
        banco_id=data.banco_id,
        tipo_cuenta_id=data.tipo_cuenta_id,
    )
    session.add(cuenta)
    session.commit()
    session.refresh(cuenta)
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