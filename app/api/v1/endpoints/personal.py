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
    return services.get_by_id(id, session)

@router.patch("/{id}", response_model=PersonalRead, status_code=status.HTTP_200_OK)
def update(id: int, datos:PersonalUpdate, session: Session = Depends(get_session))->PersonalRead:
    return services.update(id, datos, session)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, session:Session=Depends(get_session)):
    services.delete(id, session)
