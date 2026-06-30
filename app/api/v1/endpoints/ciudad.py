from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.ciudad import CiudadCreate,CiudadRead
from app.services import ciudad as services

router = APIRouter(prefix="/ciudades", tags=["ciudades"])

@router.post("/", response_model=CiudadRead, status_code=status.HTTP_201_CREATED)
def create(datos:CiudadCreate, session: Session = Depends(get_session)):
    return services.create(datos, session)

@router.get("/", response_model=list[CiudadRead])
def get_all(session: Session = Depends(get_session)) -> list[CiudadRead]:
    return services.get_all(session)

@router.get("/{id}", response_model=CiudadRead)
def get_by_id(id: int, session: Session = Depends(get_session)) -> CiudadRead:
    ciudad = services.get_by_id(id, session)

    if ciudad is None:
        raise HTTPException(status_code=404, detail='Ciudad no encontrada')
    return ciudad

@router.put("/{id}", response_model=CiudadRead)
def update(id:int, datos:CiudadCreate, session: Session = Depends(get_session)) -> CiudadRead:
    ciudad =services.update(id, datos, session)

    if ciudad is None:
        raise HTTPException(status_code=404, detail='Ciudad no encontrada')
    
    return ciudad

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, session: Session = Depends(get_session)):
    ciudad = services.delete(id, session)

    if not ciudad:
        raise HTTPException(status_code=404, detail='Ciudad no encontrada')
    
    session.delete(ciudad)
