from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.dato_bancario import DatoBancarioCreate, DatoBancarioRead
from app.services import dato_bancario as service

router = APIRouter(prefix="/datos-bancarios", tags=["datos_bancarios"])


@router.post("/", response_model=DatoBancarioRead)
def crear(data: DatoBancarioCreate, session: Session = Depends(get_session)):
    try:
        return service.crear(session, data)
    except ValueError as e:
        # El service lanzó ValueError porque una FK no existe.
        # Lo traduzco a un 404 HTTP limpio (dato malo del cliente, no error mío).
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=list[DatoBancarioRead])
def listar(session: Session = Depends(get_session)):
    return service.listar(session)


@router.get("/{cuenta_id}", response_model=DatoBancarioRead)
def obtener(cuenta_id: int, session: Session = Depends(get_session)):
    cuenta = service.obtener(session, cuenta_id)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return cuenta


@router.delete("/{cuenta_id}")
def eliminar(cuenta_id: int, session: Session = Depends(get_session)):
    if not service.eliminar(session, cuenta_id):
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return {"ok": True}