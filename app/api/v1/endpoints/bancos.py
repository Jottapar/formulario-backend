from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.banco import BancoCreate, BancoRead
from app.services import banco as banco_service

router = APIRouter(prefix="/bancos", tags=["bancos"])


@router.post("/", response_model=BancoRead, status_code=status.HTTP_201_CREATED)
def crear(datos: BancoCreate, session: Session = Depends(get_session)):
    return banco_service.crear_banco(session, datos)


@router.get("/", response_model=list[BancoRead])
def listar(session: Session = Depends(get_session)):
    return banco_service.listar_bancos(session)

@router.get("/{id}", response_model=BancoRead)
def obtener(banco_id: int, session: Session = Depends(get_session)):
    banco = banco_service.obtener_banco(session, banco_id)
    if banco is None:
        raise HTTPException(status_code=404, detail="Banco no encontrado")
    return banco


@router.put("/{id}", response_model=BancoRead)
def actualizar(banco_id: int, datos: BancoCreate, session: Session = Depends(get_session)):
    banco = banco_service.actualizar_banco(session, banco_id, datos)
    if banco is None:
        raise HTTPException(status_code=404, detail="Banco no encontrado")
    return banco


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(banco_id: int, session: Session = Depends(get_session)):
    exito = banco_service.eliminar_banco(session, banco_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Banco no encontrado")