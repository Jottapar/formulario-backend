from fastapi import APIRouter, Depends, status, HTTPException
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
    alimentacion = service.get_by_id(session, id)

    if alimentacion is None:
        raise HTTPException(status_code=404, detail='Alimentacion no encontrada')
    
    return alimentacion

@router.put("/{id}", response_model=AlimentacionRead)
def update(id: int, datos:AlimentacionCreate, session: Session = Depends(get_session)):
    alimentacion = service.update(session, id, datos)

    if alimentacion is None:
        raise HTTPException(status_code=404, detail='Alimentacion no se encuentra')
    
    return alimentacion

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, session: Session = Depends(get_session)):
    alimentacion = service.delete(session, id)

    if not alimentacion:
        raise HTTPException(status_code=404, detail='Alimentacion no encontrada')
    








