from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from datetime import datetime

from app.db.session import get_session
from app.schemas.status_personal import StatusPersonalCreate, StatusPersonalRead
from app.services import status_personal as services


router = APIRouter(prefix="/status_personal", tags=["status_personal"])


@router.post("/", response_model=StatusPersonalRead, status_code=status.HTTP_201_CREATED)
def create(datos:StatusPersonalCreate, session: Session = Depends(get_session))->StatusPersonalRead:
    return services.create(datos, session)


@router.get("/", response_model=list[StatusPersonalRead])
def get_all(session: Session = Depends(get_session))-> list[StatusPersonalRead]:
    return services.get_all(session)

@router.get("/{id}", response_model=StatusPersonalRead)
def get_by_id(id: int, session: Session = Depends(get_session))->StatusPersonalRead:
    status=services.get_by_id(id, session)

    if status is None:
        raise HTTPException(status_code=404, detail='Status No encontrado')
    
    return status

@router.put("/{id}",response_model=StatusPersonalRead,status_code=status.HTTP_200_OK)
def update(id:int, datos:StatusPersonalCreate, session: Session = Depends(get_session))->StatusPersonalRead:
    status= services.update(id,datos, session)

    if status is None:
        raise HTTPException(status_code=404, detail='Status no encontrado')
    
    return status

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, session:Session = Depends(get_session)):
    status= services.delete(id,session)

    if not status:
        raise HTTPException(status_code=404, detail='Status no encontrado')