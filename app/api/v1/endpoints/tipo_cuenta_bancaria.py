from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.tipo_cuenta_bancaria import TipoCuentaCreate, TipoCuentaRead
from app.services import tipo_cuenta_bancaria as service

router = APIRouter(prefix="/tipos-cuentas", tags=["tipos_cuentas"])


@router.post("/", response_model=TipoCuentaRead)
def crear(data: TipoCuentaCreate, session: Session = Depends(get_session)):
    return service.crear(session, data)


@router.get("/", response_model=list[TipoCuentaRead])
def listar(session: Session = Depends(get_session)):
    return service.listar(session)


@router.get("/{tipo_id}", response_model=TipoCuentaRead)
def obtener(tipo_id: int, session: Session = Depends(get_session)):
    tipo = service.obtener(session, tipo_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de cuenta no encontrado")
    return tipo


@router.put("/{tipo_id}", response_model=TipoCuentaRead)
def actualizar(tipo_id: int, data: TipoCuentaCreate, session: Session = Depends(get_session)):
    tipo = service.actualizar(session, tipo_id, data)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de cuenta no encontrado")
    return tipo


@router.delete("/{tipo_id}")
def eliminar(tipo_id: int, session: Session = Depends(get_session)):
    if not service.eliminar(session, tipo_id):
        raise HTTPException(status_code=404, detail="Tipo de cuenta no encontrado")
    return {"ok": True}