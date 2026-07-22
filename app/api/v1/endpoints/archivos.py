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
    return services.get_by_id(id, session)

@router.put("/{id}", response_model=ArchivoRead, status_code=status.HTTP_200_OK)
def update(id: int, datos: ArchivoCreate, session: Session = Depends(get_session)):
    return services.update(id, datos, session)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, session: Session = Depends(get_session)):
    services.delete(id, session)
