from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from datetime import datetime

from app.db.session import get_session
from app.schemas.personal import PersonalCreate, PersonalRead, PersonalUpdate
from app.services import personal as services

router= APIRouter(prefix="/personal", tags=["Personal"])

@router.post("/", response_model=PersonalRead, status_code=status.HTTP_201_CREATED)
def create(datos:PersonalCreate, session: Session = Depends(get_session))-> PersonalRead:
    return services.create(datos,session)

@router.get("/", response_model=list[PersonalRead])
def get_all(session: Session = Depends(get_session))-> list[PersonalCreate]:
    return services.get_all(session)

@router.get("/{id}", response_model=PersonalRead)
def get_by_id(id:int, session: Session = Depends(get_session))-> PersonalRead:
    registro= services.get_by_id(id, session)

    if registro is None:
        raise HTTPException(status_code=404, detail='Persona no existe')
    
    return registro

@router.patch("/{id}", response_model=PersonalRead, status_code=status.HTTP_200_OK)
def update(id: int, datos:PersonalUpdate, session: Session = Depends(get_session))->PersonalRead:
    registro = services.update(id, datos, session)

    if registro is None:
        raise HTTPException(status_code=404, detail='La persona no existe')
    
    return registro

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, session:Session=Depends(get_session)):
    registro = services.delete(id, session)

    if not registro:
        raise HTTPException(status_code=404, detail='Persona no existe')   