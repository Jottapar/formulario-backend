from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.genero import GeneroCreate, GeneroRead
from app.services import genero as services

router= APIRouter(prefix="/generos", tags=["generos"])

@router.post("/", response_model=GeneroRead,status_code=status.HTTP_201_CREATED)
def create(datos:GeneroCreate, session: Session = Depends(get_session))->GeneroRead:
    return services.create(datos, session)

@router.get("/", response_model=list[GeneroRead])
def get_all(session: Session = Depends(get_session))->list[GeneroRead]:
    return services.get_all(session)

@router.get("/{id}", response_model=GeneroRead, status_code=status.HTTP_200_OK)
def get_by_id(id: int, session: Session = Depends(get_session))-> GeneroRead:
    return services.get_by_id(id, session)

@router.put("/{id}", response_model=GeneroRead)
def update(id:int, datos: GeneroCreate, session: Session=Depends(get_session))-> GeneroRead:
    return services.update(id, datos, session)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, session: Session = Depends(get_session)):
    services.delete(id, session)

