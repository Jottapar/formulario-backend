from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from datetime import datetime

from app.db.session import get_session
from app.schemas.eps import EpsCreate,EpsRead
from app.services import eps as services

router=APIRouter(prefix="/eps", tags=["eps"])

@router.post("/", response_model=EpsRead, status_code=status.HTTP_201_CREATED)
def create(datos:EpsCreate, session: Session = Depends(get_session))-> EpsRead:
    return services.create(datos, session)

@router.get("/", response_model=list[EpsRead])
def get_all(session: Session = Depends(get_session))->list[EpsRead]:
    return services.get_all(session)

@router.get("/{id}", response_model=EpsRead,status_code=status.HTTP_200_OK)
def get_by_id(id:int, session:Session=Depends(get_session))->EpsRead:
    eps=services.get_by_id(id, session)

    if eps is None:
        raise HTTPException(status_code=404, detail='Eps no encontrada')
    
    return eps

@router.put("/{id}", response_model=EpsRead)
def update(id:int, datos:EpsCreate, session:Session = Depends(get_session)) -> EpsRead :
    eps = services.update(id,datos,session)

    if eps is None:
        raise HTTPException(id, datos, session)
    
    return eps

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, session:Session = Depends(get_session)):
    eps = services.delete(id,session)

    if not eps:
        raise HTTPException(status_code=404, detail='Eps no encontrada')