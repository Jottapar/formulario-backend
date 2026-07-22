from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.tipo_cuenta_bancaria import TipoCuentaCreate, TipoCuentaRead
from app.services import tipo_cuenta_bancaria as services

router = APIRouter(prefix="/tipos-cuentas", tags=["tipos_cuentas"])


@router.post("/", response_model=TipoCuentaRead)
def create(data: TipoCuentaCreate, session: Session = Depends(get_session)):
    return services.creatr(session, data)


@router.get("/", response_model=list[TipoCuentaRead])
def get_all(session: Session = Depends(get_session)):
    return services.get_all(session)


@router.get("/{id}", response_model=TipoCuentaRead)
def get_by_id(id: int, session: Session = Depends(get_session)):
    return services.get_by_id(id, session)


@router.put("/{id}", response_model=TipoCuentaRead)
def update(id: int, data: TipoCuentaCreate, session: Session = Depends(get_session)):
    return services.update(id, data, session)

@router.delete("/{id}")
def eliminar(id: int, session: Session = Depends(get_session)):
    services.delete(id, session)