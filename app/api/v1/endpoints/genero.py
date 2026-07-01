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
    genero = services.get_by_id(id, session)

    if genero is None:
        raise HTTPException(status_code=404, detail='Este genero no se encontro')
    
    return genero

@router.put("/{id}", response_model=GeneroRead)
def update(id:int, datos: GeneroCreate, session: Session=Depends(get_session))-> GeneroRead:
    genero = services.update(id, datos, session)

    if genero is None:
        raise HTTPException(status_code=404, detail='Genero no encontrado')
    
    return genero

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, session: Session = Depends(get_session)):
    genero = services.delete(id, session)

    if not genero:
        raise HTTPException(status_code=404,detail='Genero no encontrado')
    
