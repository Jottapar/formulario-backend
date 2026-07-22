from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.dato_bancario import DatoBancarioCreate, DatoBancarioRead
from app.services import dato_bancario as services

router = APIRouter(prefix="/datos-bancarios", tags=["datos_bancarios"])


@router.post("/", response_model=DatoBancarioRead)
def create(data: DatoBancarioCreate, session: Session = Depends(get_session)):
    return services.create(session, data)

@router.get("/", response_model=list[DatoBancarioRead])
def get_all(session: Session = Depends(get_session)):
    return services.get_all(session)


@router.get("/{id}", response_model=DatoBancarioRead)
def get_by_id(id: int, session: Session = Depends(get_session)):
    cuenta = services.get_by_id(id, session)
    return cuenta


@router.delete("/{id}")
def delete(id: int, session: Session = Depends(get_session)):
    services.delete(id, session)
     