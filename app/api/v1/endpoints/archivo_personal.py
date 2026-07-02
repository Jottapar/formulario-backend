from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.archivo_personal import ArchivoPersonalCreate, ArchivoPersonalRead, ArchivoPersonalUpdate
from app.services import archivo_personal as services


router= APIRouter(prefix="/archivos_personales", tags=["archivos_personales"])

@router.post("/", response_model=ArchivoPersonalRead, status_code=status.HTTP_201_CREATED)
def create(datos:ArchivoPersonalCreate, session:Session=Depends(get_session)):
    return services.create(datos, session)


@router.get("/", response_model=list[ArchivoPersonalRead])
def get_all(session: Session = Depends(get_session)):
    return services.get_all(session)


@router.get("/{id}", response_model=list[ArchivoPersonalRead])
def get_by_personal_id(id: int, session:Session = Depends(get_session)):
    consulta = services.get_by_personal_id(id,session)

    if not consulta:
        raise HTTPException(status_code=404, detail='Personal no tiene Aarchivos relacionados')

    return consulta


@router.patch("/{id}", response_model=ArchivoPersonalRead, status_code=status.HTTP_200_OK)
def update_url(id: int, datos:ArchivoPersonalUpdate, session: Session = Depends(get_session)):
    new_update = services.update_url(id, datos, session)

    if new_update is None:
        raise HTTPException(status_code=404, detail='No hay archivos relacionados de esa persona')
    
    return new_update

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, session: Session = Depends(get_session)):
    registro = services.delete(id,session)

    if not registro:
        raise HTTPException(status_code=404, detail='archivo de la persona no encontrado')

