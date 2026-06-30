from sqlmodel import Session, select
from datetime import datetime
from app.models.banco import Banco
from app.schemas.banco import BancoCreate


def crear_banco(session: Session, datos: BancoCreate) -> Banco:
    # 1. Convertir el schema de entrada en un objeto de la tabla
    banco = Banco(nombre=datos.nombre)
    session.add(banco)
    session.commit()
    session.refresh(banco)

    return banco


def listar_bancos(session: Session) -> list[Banco]:
    # Construye y ejecuta un SELECT * FROM bancos
    consulta = select(Banco)
    resultados = session.exec(consulta).all()
    return resultados

def obtener_banco(session: Session, banco_id: int) -> Banco | None:
    return session.get(Banco, banco_id)


def actualizar_banco(session: Session, banco_id: int, datos: BancoCreate) -> Banco | None:
    banco = session.get(Banco, banco_id)
    if banco is None:
        return None
    banco.nombre = datos.nombre
    banco.updated_at = datetime.now()
    session.add(banco)
    session.commit()
    session.refresh(banco)
    return banco


def eliminar_banco(session: Session, banco_id: int) -> bool:
    banco = session.get(Banco, banco_id)
    if banco is None:
        return False
    session.delete(banco)
    session.commit()
    return True