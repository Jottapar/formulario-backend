from sqlmodel import Session, select
from app.models.tipo_cuenta_bancaria import TipoCuentaBancaria
from app.schemas.tipo_cuenta_bancaria import TipoCuentaCreate


def crear(session: Session, data: TipoCuentaCreate) -> TipoCuentaBancaria:
    tipo = TipoCuentaBancaria(nombre=data.nombre)
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo


def listar(session: Session) -> list[TipoCuentaBancaria]:
    return session.exec(select(TipoCuentaBancaria)).all()


def obtener(session: Session, tipo_id: int) -> TipoCuentaBancaria | None:
    return session.get(TipoCuentaBancaria, tipo_id)


def actualizar(session: Session, tipo_id: int, data: TipoCuentaCreate) -> TipoCuentaBancaria | None:
    tipo = session.get(TipoCuentaBancaria, tipo_id)
    if not tipo:
        return None
    tipo.nombre = data.nombre
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo


def eliminar(session: Session, tipo_id: int) -> bool:
    tipo = session.get(TipoCuentaBancaria, tipo_id)
    if not tipo:
        return False
    session.delete(tipo)
    session.commit()
    return True

