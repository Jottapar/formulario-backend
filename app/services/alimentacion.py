from sqlmodel import Session, select
from datetime import datetime
from app.models.alimentacion import Alimentacion
from app.schemas.alimentacion import AlimentacionCreate, AlimentacionRead

def create(session:Session, datos: AlimentacionCreate) -> Alimentacion:
    alimentacion = Alimentacion(nombre= datos.nombre)
    session.add(alimentacion)
    session.commit()
    session.refresh(alimentacion)
    return alimentacion

def get_all(session:Session) -> list[Alimentacion]:
    consulta = select(Alimentacion)
    resultados = session.exec(consulta).all()
    return resultados

def get_by_id(session:Session, id: int) -> Alimentacion | None:
    return session.get(Alimentacion,id)

def update(session:Session, id: int, datos:AlimentacionCreate ) -> Alimentacion | None:
    consulta = session.get(Alimentacion, id)

    if consulta is None:
        return None
    
    consulta.nombre = datos.nombre
    consulta.updated_at = datetime.now()
    session.add(consulta)
    session.commit()
    session.refresh(consulta)
    return consulta

def delete(session: Session, id:int) -> bool:
    consulta = session.get(Alimentacion, id)

    if consulta is None:
        return False
    
    session.delete(consulta)
    session.commit()
    return True
