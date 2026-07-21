from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.alimentacion import AlimentacionCreate, AlimentacionRead
from app.services import alimentacion as service

router = APIRouter (prefix="/alimentaciones", tags=["alimentaciones"])


@router.post("/", response_model=AlimentacionRead, status_code=status.HTTP_201_CREATED)
def create(datos:AlimentacionCreate, session: Session = Depends(get_session)):
    return service.create(session, datos)

@router.get("/", response_model=list[AlimentacionRead])
def get_all(session: Session = Depends(get_session)):
    return service.get_all(session)

@router.get("/{id}", response_model=AlimentacionRead)
def get_by_id(id: int, session: Session = Depends(get_session)):
    return service.get_by_id(session, id)

@router.put("/{id}", response_model=AlimentacionRead)
def update(id: int, datos: AlimentacionCreate, session: Session = Depends(get_session)):
    return service.update(session, id, datos)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, session: Session = Depends(get_session)):
    service.delete(session, id)
    








