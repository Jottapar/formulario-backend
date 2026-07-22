from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.banco import BancoCreate, BancoRead
from app.services import banco as services

router = APIRouter(prefix="/bancos", tags=["bancos"])


@router.post("/", response_model=BancoRead, status_code=status.HTTP_201_CREATED)
def create(datos: BancoCreate, session: Session = Depends(get_session)):
    return services.create(session, datos)

@router.get("/", response_model=list[BancoRead])
def get_all(session: Session = Depends(get_session)):
    return services.get_all(session)

@router.get("/{id}", response_model=BancoRead)
def get_by_id(banco_id: int, session: Session = Depends(get_session)):
    return services.get_by_id(session, banco_id)

@router.put("/{id}", response_model=BancoRead)
def update(banco_id: int, datos: BancoCreate, session: Session = Depends(get_session)):
    return services.update(session, banco_id, datos)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(banco_id: int, session: Session = Depends(get_session)):
    services.delete(session, banco_id)
    