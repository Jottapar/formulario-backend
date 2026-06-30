from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.archivo import ArchivoCreate,ArchivoRead
from app.services import archivos as services

router = APIRouter(prefix="/archivos", tags=["archivos"])

@router.post("/", response_model=ArchivoRead, status_code=status.HTTP_201_CREATED)
def create(datos:ArchivoCreate, session: Session = Depends(get_session)):
    return services.create(session, datos)

@router.get("/", response_model=list[ArchivoRead])
def get_all(session: Session = Depends(get_session)):
    return services.get_all(session)

@router.get("/{id}", response_model=ArchivoRead)
def get_by_id(id: int, session:Session = Depends(get_session)):
    archivo = services.get_by_id(id, session)

    if archivo is None:
        raise HTTPException(status_code=404, detail='Archivo no encontrado')
    
    return archivo

@router.put("/{id}", response_model=ArchivoRead, status_code=status.HTTP_200_OK)
def update(id: int, datos: ArchivoCreate, session: Session = Depends(get_session)):
    archivo = services.update(id, datos, session)

    if archivo is None:
        raise HTTPException(status_code=404, detail='Archivo no encontrado')
    
    return archivo

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, session: Session = Depends(get_session)):
    archivo = services.delete(id, session)

    if not archivo:
        raise HTTPException(status_code=404, detail='Archivo no encontrado')
