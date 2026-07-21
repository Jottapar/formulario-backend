CONTENIDO DEL PROYECTO


--- FILE: app/__init__.py ---

```python

```

--- FILE: app/main.py ---

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings

from app.utils.logger import logger
from app.utils.errors import NotFoundError, AlreadyExistsError, BussinesError, DatabaseError
from app.utils.handlers import not_found_handler, already_exists_handler, bussines_error_handler,database_error_handler


from app.api.hub import api_hub




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que corre al ARRANCAR la app
    print("Iniciando aplicación: creando tablas...")
    yield
    # Código que corre al APAGAR la app
    print("Apagando aplicación...")



app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)




app.add_exception_handler(NotFoundError, not_found_handler)
app.add_exception_handler(AlreadyExistsError, already_exists_handler)
app.add_exception_handler(BussinesError, bussines_error_handler)
app.add_exception_handler(DatabaseError, database_error_handler)

app.include_router(api_hub)



@app.get("/")
def raiz():
    return {"mensaje": "API del formulario funcionando", "version": settings.VERSION}
```

--- FILE: app/api/__init__.py ---

```python

```

--- FILE: app/api/hub.py ---

```python
from fastapi import APIRouter

from app.api.v1.router import router_v1
from app.core.config import settings

api_hub = APIRouter()

api_hub.include_router(router_v1, prefix=settings.API_V1_STR)
```

--- FILE: app/api/v1/__init__.py ---

```python

```

--- FILE: app/api/v1/router.py ---

```python
from fastapi import APIRouter

from app.api.v1.endpoints import bancos, tipo_cuenta_bancaria, dato_bancario, alimentacion, archivos, ciudad, eps, genero, status_personal, archivo_personal, personal

router_v1 = APIRouter()

router_v1.include_router(bancos.router)
router_v1.include_router(tipo_cuenta_bancaria.router)
router_v1.include_router(dato_bancario.router)
router_v1.include_router(alimentacion.router)
router_v1.include_router(archivos.router)
router_v1.include_router(ciudad.router)
router_v1.include_router(eps.router)
router_v1.include_router(genero.router)
router_v1.include_router(status_personal.router)
router_v1.include_router(archivo_personal.router)
router_v1.include_router(personal.router)
```

--- FILE: app/api/v1/endpoints/__init__.py ---

```python

```

--- FILE: app/api/v1/endpoints/alimentacion.py ---

```python
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.alimentacion import AlimentacionCreate, AlimentacionRead
from app.services import alimentacion as service

router = APIRouter (prefix="/alimentaciones", tags=["alimentaciones"])


@router.post("/", response_model=AlimentacionRead, status_code=status.HTTP_201_CREATED)
def create(datos:AlimentacionCreate, session: Session = Depends(get_session)):
    return service.create(session, datos)

@router.get("/", response_model=list[AlimentacionRead])
def get_all(session: Session = Depends(get_session)):
    return service.get_all(session)

@router.get("/{id}", response_model=AlimentacionRead)
def get_by_id(id: int, session: Session = Depends(get_session)):
    alimentacion = service.get_by_id(session, id)

    if alimentacion is None:
        raise HTTPException(status_code=404, detail='Alimentacion no encontrada')
    
    return alimentacion

@router.put("/{id}", response_model=AlimentacionRead)
def update(id: int, datos:AlimentacionCreate, session: Session = Depends(get_session)):
    alimentacion = service.update(session, id, datos)

    if alimentacion is None:
        raise HTTPException(status_code=404, detail='Alimentacion no se encuentra')
    
    return alimentacion

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, session: Session = Depends(get_session)):
    alimentacion = service.delete(session, id)

    if not alimentacion:
        raise HTTPException(status_code=404, detail='Alimentacion no encontrada')
    









```

--- FILE: app/api/v1/endpoints/archivo_personal.py ---

```python
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


```

--- FILE: app/api/v1/endpoints/archivos.py ---

```python
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

```

--- FILE: app/api/v1/endpoints/bancos.py ---

```python
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.banco import BancoCreate, BancoRead
from app.services import banco as banco_service

router = APIRouter(prefix="/bancos", tags=["bancos"])


@router.post("/", response_model=BancoRead, status_code=status.HTTP_201_CREATED)
def crear(datos: BancoCreate, session: Session = Depends(get_session)):
    return banco_service.crear_banco(session, datos)


@router.get("/", response_model=list[BancoRead])
def listar(session: Session = Depends(get_session)):
    return banco_service.listar_bancos(session)

@router.get("/{id}", response_model=BancoRead)
def obtener(banco_id: int, session: Session = Depends(get_session)):
    banco = banco_service.obtener_banco(session, banco_id)
    if banco is None:
        raise HTTPException(status_code=404, detail="Banco no encontrado")
    return banco


@router.put("/{id}", response_model=BancoRead)
def actualizar(banco_id: int, datos: BancoCreate, session: Session = Depends(get_session)):
    banco = banco_service.actualizar_banco(session, banco_id, datos)
    if banco is None:
        raise HTTPException(status_code=404, detail="Banco no encontrado")
    return banco


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(banco_id: int, session: Session = Depends(get_session)):
    exito = banco_service.eliminar_banco(session, banco_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Banco no encontrado")
```

--- FILE: app/api/v1/endpoints/ciudad.py ---

```python
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
    

```

--- FILE: app/api/v1/endpoints/dato_bancario.py ---

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.dato_bancario import DatoBancarioCreate, DatoBancarioRead
from app.services import dato_bancario as service

router = APIRouter(prefix="/datos-bancarios", tags=["datos_bancarios"])


@router.post("/", response_model=DatoBancarioRead)
def crear(data: DatoBancarioCreate, session: Session = Depends(get_session)):
    try:
        return service.crear(session, data)
    except ValueError as e:
        # El service lanzó ValueError porque una FK no existe.
        # Lo traduzco a un 404 HTTP limpio (dato malo del cliente, no error mío).
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=list[DatoBancarioRead])
def listar(session: Session = Depends(get_session)):
    return service.listar(session)


@router.get("/{cuenta_id}", response_model=DatoBancarioRead)
def obtener(cuenta_id: int, session: Session = Depends(get_session)):
    cuenta = service.obtener(session, cuenta_id)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return cuenta


@router.delete("/{cuenta_id}")
def eliminar(cuenta_id: int, session: Session = Depends(get_session)):
    if not service.eliminar(session, cuenta_id):
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return {"ok": True}
```

--- FILE: app/api/v1/endpoints/eps.py ---

```python
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
```

--- FILE: app/api/v1/endpoints/genero.py ---

```python
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
    

```

--- FILE: app/api/v1/endpoints/personal.py ---

```python
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
```

--- FILE: app/api/v1/endpoints/status_personal.py ---

```python
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
```

--- FILE: app/api/v1/endpoints/tipo_cuenta_bancaria.py ---

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.tipo_cuenta_bancaria import TipoCuentaCreate, TipoCuentaRead
from app.services import tipo_cuenta_bancaria as service

router = APIRouter(prefix="/tipos-cuentas", tags=["tipos_cuentas"])


@router.post("/", response_model=TipoCuentaRead)
def crear(data: TipoCuentaCreate, session: Session = Depends(get_session)):
    return service.crear(session, data)


@router.get("/", response_model=list[TipoCuentaRead])
def listar(session: Session = Depends(get_session)):
    return service.listar(session)


@router.get("/{tipo_id}", response_model=TipoCuentaRead)
def obtener(tipo_id: int, session: Session = Depends(get_session)):
    tipo = service.obtener(session, tipo_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de cuenta no encontrado")
    return tipo


@router.put("/{tipo_id}", response_model=TipoCuentaRead)
def actualizar(tipo_id: int, data: TipoCuentaCreate, session: Session = Depends(get_session)):
    tipo = service.actualizar(session, tipo_id, data)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de cuenta no encontrado")
    return tipo


@router.delete("/{tipo_id}")
def eliminar(tipo_id: int, session: Session = Depends(get_session)):
    if not service.eliminar(session, tipo_id):
        raise HTTPException(status_code=404, detail="Tipo de cuenta no encontrado")
    return {"ok": True}
```

--- FILE: app/core/__init__.py ---

```python

```

--- FILE: app/core/config.py ---

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- App ---
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str

    # --- Database (piezas sueltas del .env) ---
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    # --- Security (para cuando lleguemos a JWT) ---
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # La DATABASE_URL se arma a partir de las piezas
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Le decimos a Pydantic de dónde leer las variables
    model_config = SettingsConfigDict(env_file=".env")


# Una sola instancia que toda la app importará
settings = Settings()
```

--- FILE: app/db/__init__.py ---

```python

```

--- FILE: app/db/session.py ---

```python
from sqlmodel import SQLModel, Session, create_engine

from app.core.config import settings
import app.models
 

# 1. El ENGINE: la fábrica de conexiones. Se crea UNA sola vez.
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # imprime el SQL que ejecuta (útil para aprender)
)

# 3. La DEPENDENCY: presta una session por petición y la cierra sola.
def get_session():
    with Session(engine) as session:
        yield session
```

--- FILE: app/models/__init__.py ---

```python
from .banco import Banco
from .tipo_cuenta_bancaria import TipoCuentaBancaria
from .dato_bancario import DatoBancario
from .genero import Genero
from .eps import Eps
from .alimentacion import Alimentacion
from .archivos import Archivos
from .archivos_personal import ArchivosPersonal
from .ciudad import Ciudad
from .personal import Personal
from .status_personal import StatusPersonal
from .usuario import Usuario
from .rol import Rol


__all__ = ["Banco", "TipoCuentaBancaria", "DatoBancario", "Genero", "Eps", "Alimentacion", 
           "Archivos", "ArchivosPersonal","Ciudad", "Personal", "StatusPersonal", 'Usuario', 'Rol'
           ]
```

--- FILE: app/models/alimentacion.py ---

```python
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .personal import Personal

class Alimentacion(SQLModel, table=True):
    __tablename__= "alimentaciones"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=15)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    personal: list[Personal] = Relationship(back_populates="alimentacion")


```

--- FILE: app/models/archivos.py ---

```python
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .archivos_personal import ArchivosPersonal

class Archivos(SQLModel, table=True):
    __tablename__= "archivos"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=25)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


    archivos_personal: list[ArchivosPersonal] = Relationship(back_populates="archivos")
```

--- FILE: app/models/archivos_personal.py ---

```python
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .personal import Personal
    from .archivos import Archivos

class ArchivosPersonal(SQLModel, table=True):
    __tablename__= "archivos_personal"
    __table_args__= (
        UniqueConstraint("personal_id","archivos_id", name="uq_persona_tipo"),
    )

    id: int | None = Field(default=None, primary_key=True)
    personal_id: int = Field(foreign_key="personal.id")
    archivos_id: int = Field(foreign_key="archivos.id")
    url: str

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    personal: "Personal" = Relationship(back_populates="archivos_personal")
    archivos: "Archivos" = Relationship(back_populates="archivos_personal")
```

--- FILE: app/models/banco.py ---

```python
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .dato_bancario import DatoBancario



class Banco(SQLModel, table=True):
    __tablename__ = "bancos"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=15)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    datos_bancarios: list["DatoBancario"] = Relationship(back_populates="banco")
```

--- FILE: app/models/ciudad.py ---

```python
from datetime import datetime 
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .personal import Personal

class Ciudad(SQLModel, table=True):
    __tablename__= "ciudades"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    personal: list[Personal] = Relationship(back_populates="ciudad")


```

--- FILE: app/models/dato_bancario.py ---

```python
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .banco import Banco
    from .tipo_cuenta_bancaria import TipoCuentaBancaria
    from .personal import Personal


class DatoBancario(SQLModel, table=True):
    __tablename__ = "datos_bancarios"

    id: int | None = Field(default=None, primary_key=True)
    num_cuenta: str = Field(index=True)

    banco_id: int = Field(foreign_key="bancos.id")
    tipo_cuenta_id: int = Field(foreign_key="tipos_cuentas_bancarias.id")
    personal_id: int = Field(foreign_key="personal.id") 

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # --- Navegación Python (lado "MUCHOS": van SIN lista, es un solo objeto) ---
    banco: "Banco" = Relationship(back_populates="datos_bancarios")
    tipo_cuenta: "TipoCuentaBancaria" = Relationship(back_populates="datos_bancarios")
    personal: "Personal" = Relationship(back_populates="datos_bancarios")
```

--- FILE: app/models/eps.py ---

```python
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .personal import Personal

class Eps(SQLModel, table=True):
    __tablename__="eps"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    personal: list[Personal] = Relationship(back_populates="eps")

     
```

--- FILE: app/models/genero.py ---

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.personal import Personal


class Genero (SQLModel, table=True):
    __tablename__= "generos"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=15)

    created_at: datetime = Field(default_factory= datetime.now)
    updated_at: datetime = Field(default_factory= datetime.now)

    personal: list[Personal] = Relationship(back_populates="genero")

```

--- FILE: app/models/personal.py ---

```python
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from typing import TYPE_CHECKING



if TYPE_CHECKING:
     from app.models.genero import Genero
     from app.models.alimentacion import Alimentacion
     from app.models.ciudad import Ciudad
     from app.models.eps import Eps
     from app.models.status_personal import StatusPersonal
     from app.models.dato_bancario import DatoBancario
     from app.models.archivos_personal import ArchivosPersonal

class Personal(SQLModel, table=True):
    __tablename__= "personal"

    id: int | None = Field(default=None, primary_key=True)
    tipo_doc: str = Field(max_length=3)
    num_doc: str = Field(max_length=10)
    primer_nombre: str
    segundo_nombre: str | None
    primer_apellido: str
    segundo_apellido: str | None
    telefono: str
    fecha_nacimiento: date
    correo: EmailStr
    ciudad: str
    direccion: str = Field(max_length=100)
    nombre_emergencia: str
    telefono_emergencia: str
    estatura: int
    talla_camiseta: str
    talla_pantalon: str
    talla_zapatos: str
    alergias: str
    nivel_ingles: str

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    genero_id: int = Field(foreign_key="generos.id")
    alimentacion_id: int = Field(foreign_key="alimentaciones.id")
    ciudad_id: int = Field(foreign_key="ciudades.id")
    eps_id: int = Field(foreign_key="eps.id")
    status_personal_id: int = Field(foreign_key="status_personal.id")

    genero: "Genero" = Relationship(back_populates="personal")
    datos_bancarios: list[DatoBancario] = Relationship(back_populates="personal")
    ciudad: "Ciudad" = Relationship(back_populates="personal")
    eps: "Eps" = Relationship(back_populates="personal")
    alimentacion: "Alimentacion" = Relationship(back_populates="personal")
    status_personal: "StatusPersonal" = Relationship(back_populates="personal")
    archivos_personal: list[ArchivosPersonal] = Relationship(back_populates="personal")


```

--- FILE: app/models/rol.py ---

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from pydantic import EmailStr
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.usuario import Usuario


class Rol(SQLModel, table=True):
    __tablename__='roles'

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=25)
    status: bool = Field(default=True)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory= datetime.now)

    usuarios: list[Usuario] = Relationship(back_populates='rol')
```

--- FILE: app/models/status_personal.py ---

```python
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .personal import Personal

class StatusPersonal(SQLModel, table=True):
    __tablename__= "status_personal"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=15)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    personal: list[Personal] = Relationship(back_populates="status_personal")
```

--- FILE: app/models/tipo_cuenta_bancaria.py ---

```python
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .dato_bancario import DatoBancario

class TipoCuentaBancaria(SQLModel, table=True):
    __tablename__ = "tipos_cuentas_bancarias"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


    datos_bancarios: list["DatoBancario"] = Relationship(back_populates="tipo_cuenta")
```

--- FILE: app/models/usuario.py ---

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from pydantic import EmailStr
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.rol import Rol


class Usuario(SQLModel,table= True):
    __tablename__='usuarios'

    id: int| None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=25)
    apellido: str = Field(max_length=25)
    correo: EmailStr = Field(max_length=100)
    password: str
    rol_id: int = Field(foreign_key= 'roles.id')

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory= datetime.now)

    rol: 'Rol' = Relationship(back_populates='usuarios')
```

--- FILE: app/schemas/__init__.py ---

```python

```

--- FILE: app/schemas/alimentacion.py ---

```python
from datetime import datetime
from sqlmodel import SQLModel

class AlimentacionBase(SQLModel):
    nombre: str

class AlimentacionCreate(AlimentacionBase):
    pass 

class AlimentacionRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime
    
```

--- FILE: app/schemas/archivo.py ---

```python
from datetime import datetime
from sqlmodel import SQLModel

class ArchivoBase(SQLModel):
    nombre: str

class ArchivoCreate(ArchivoBase):
    pass

class ArchivoRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    created_at: datetime


```

--- FILE: app/schemas/archivo_personal.py ---

```python
from datetime import datetime
from sqlmodel import SQLModel

from app.schemas.personal import PersonalRead
from app.schemas.archivo import ArchivoRead

class ArchivoPersonalBase(SQLModel):
    personal_id: int
    archivos_id: int
    url: str

class ArchivoPersonalCreate(ArchivoPersonalBase):
    pass

class ArchivoPersonalRead(SQLModel):
    id: int
    personal: PersonalRead
    archivos: ArchivoRead
    url: str
    created_at: datetime
    updated_at: datetime

    

class ArchivoPersonalUpdate(SQLModel):
    url: str | None = None
```

--- FILE: app/schemas/banco.py ---

```python
from datetime import datetime
from sqlmodel import SQLModel

class BancoBase(SQLModel):
    nombre: str

class BancoCreate(BancoBase):
    pass

class BancoRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime 
    updated_at: datetime


```

--- FILE: app/schemas/ciudad.py ---

```python
from datetime import datetime
from sqlmodel import SQLModel

class CiudadBase(SQLModel):
    nombre: str

class CiudadCreate(CiudadBase):
    pass

class CiudadRead(SQLModel):
    id: int 
    nombre: str
    created_at: datetime
    updated_at: datetime


```

--- FILE: app/schemas/dato_bancario.py ---

```python
from datetime import datetime
from sqlmodel import SQLModel

from app.schemas.banco import BancoRead
from app.schemas.tipo_cuenta_bancaria import TipoCuentaRead

class DatoBancarioBase(SQLModel):
    num_cuenta: str
    banco_id: int
    tipo_cuenta_id: int

class DatoBancarioCreate(DatoBancarioBase):
    pass

class DatoBancarioRead(SQLModel):
    id: int
    num_cuenta: str
    banco: BancoRead
    tipo_cuenta: TipoCuentaRead
    created_at: datetime 
    updated_at: datetime




```

--- FILE: app/schemas/eps.py ---

```python
from datetime import datetime
from sqlmodel import SQLModel


class EpsBase(SQLModel):
    nombre: str

class EpsCreate(EpsBase):
    pass

class EpsRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime


```

--- FILE: app/schemas/genero.py ---

```python
from datetime import datetime
from sqlmodel import SQLModel

class GeneroBase(SQLModel):
    nombre: str

class GeneroCreate(GeneroBase):
    pass

class GeneroRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime


```

--- FILE: app/schemas/personal.py ---

```python
from datetime import datetime, date
from sqlmodel import SQLModel, Field
from pydantic import EmailStr

from .genero import GeneroRead
from .alimentacion import AlimentacionRead
from .ciudad import CiudadRead
from .eps import EpsRead
from .status_personal import StatusPersonalRead
from .dato_bancario import DatoBancarioRead


class PersonalBase(SQLModel):
    tipo_doc: str = Field(max_length=3)
    num_doc: str = Field(max_length=10)
    primer_nombre: str
    segundo_nombre: str | None
    primer_apellido: str
    segundo_apelido: str | None
    telefono: str
    fecha_nacimiento: date
    correo: EmailStr
    direccion: str = Field(max_length=100)
    nombre_emergencia: str = Field(max_length=100)
    telefono_emergencia: str = Field(max_length=13)
    estatura: int
    talla_camiseta: str
    talla_pantalon: str
    talla_zapatos: str
    alergias: str
    nivel_ingles: str
    
    
    genero_id: int
    alimentacion_id: int
    ciudad_id: int
    eps_id: int
    status_personal_id: int
    

class PersonalCreate(PersonalBase):
    pass
    

class PersonalRead(SQLModel):
    id: int
    tipo_doc: str
    num_doc: str
    primer_nombre: str
    segundo_nombre: str | None
    primer_apellido: str
    segundo_apellido: str | None
    telefono: str
    fecha_nacimiento: date
    correo: EmailStr
    direccion: str
    nombre_emergencia: str
    telefono_emergencia: str
    estatura: int
    talla_camiseta: str
    talla_pantalon: str
    talla_zapatos: str
    alergias: str
    nivel_ingles: str

    created_at: datetime
    updated_at: datetime

    genero: GeneroRead
    alimentacion: AlimentacionRead
    ciudad: CiudadRead
    eps: EpsRead
    status_personal: StatusPersonalRead
    datos_bancarios: list[DatoBancarioRead]


class PersonalUpdate(SQLModel):
    tipo_doc: str | None = Field(default=None, max_length=3)  
    num_doc: str | None = Field(default=None,max_length=10)
    primer_nombre: str | None = None
    segundo_nombre: str | None = None
    primer_apellido: str | None = None
    segundo_apelido: str | None = None
    telefono: str | None = None
    fecha_nacimiento: date | None = None
    correo: EmailStr | None = None
    direccion: str | None = Field(default=None,max_length=100)
    nombre_emergencia: str | None = Field(default=None,max_length=100)
    telefono_emergencia: str | None = Field(default=None,max_length=13)
    estatura: int | None = None
    talla_camiseta: str | None = None
    talla_pantalon: str | None = None
    talla_zapatos: str | None = None
    alergias: str | None = None
    nivel_ingles: str | None = None
    

    genero_id: int | None = None
    alimentacion_id: int | None = None
    ciudad_id: int | None = None
    eps_id: int | None = None
    status_personal_id: int | None = None


    
```

--- FILE: app/schemas/rol.py ---

```python
from sqlmodel import SQLModel
from datetime import datetime

from app.models.rol import Rol

class RolBase(SQLModel):
    nombre: str
    status: bool

class RolCreate(RolBase):
    pass 

class RolRead(SQLModel):
    id: int
    nombre: str
    status: bool
    created_at: datetime
    updated_at: datetime

```

--- FILE: app/schemas/status_personal.py ---

```python
from datetime import datetime
from sqlmodel import SQLModel


class StatusPersonalBase(SQLModel):
    nombre:str

class StatusPersonalCreate(StatusPersonalBase):
    pass

class StatusPersonalRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime
```

--- FILE: app/schemas/tipo_cuenta_bancaria.py ---

```python
from datetime import datetime
from sqlmodel import SQLModel


class TipoCuentaBase(SQLModel):
    nombre: str

class TipoCuentaCreate(TipoCuentaBase):
    pass


class TipoCuentaRead(SQLModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime
```

--- FILE: app/schemas/usuario.py ---

```python
from sqlmodel import SQLModel
from datetime import datetime
from pydantic import EmailStr
from app.models.usuario import Usuario

class UsuarioBase(SQLModel):
    nombre: str 
    apellido: str 
    correo: EmailStr
    password: str 
    rol_id: int


class UsuarioCreate(UsuarioBase):
    pass 

class UsuarioRead(SQLModel):
    id: int
    nombre: str 
    apellido: str 
    correo: EmailStr
    rol_id: int

    created_at: datetime
    updated_at: datetime

```

--- FILE: app/services/__init__.py ---

```python

```

--- FILE: app/services/alimentacion.py ---

```python
from sqlmodel import Session, select
from datetime import datetime
from app.models.alimentacion import Alimentacion
from app.schemas.alimentacion import AlimentacionCreate, AlimentacionRead

from app.utils.logger import logger
from app.utils.errors import NotFoundError, AlreadyExistsError, BussinesError, DatabaseError


def create(session:Session, datos: AlimentacionCreate) -> Alimentacion:
    logger.debug(f'Creando alimentacion {datos.model_dump()}')
    alimentacion = Alimentacion(nombre= datos.nombre)
    session.add(alimentacion)
    session.commit()
    session.refresh(alimentacion)
    logger.info(f'Alimentacion creada correctamente | id: {alimentacion.id} | nombre: {alimentacion.nombre}')
    return alimentacion

def get_all(session:Session) -> list[Alimentacion]:
    logger.debug(f'Buscando todas las alimentaciones')
    consulta = select(Alimentacion)
    resultados = session.exec(consulta).all()
    logger.info(f'Mostrando todas las alimentaciones')
    return resultados


def get_by_id(session:Session, id: int) -> Alimentacion | None:
    logger.debug(f'Buscando el id {id} en la tabla alimentaciones')
    consulta = session.get(Alimentacion, id)

    if not consulta:
        raise NotFoundError(Alimentacion.nombre, id)
    
    logger.info(f'Alimentacion: {consulta.nombre} encontrada con su id{consulta.id}')
    return consulta


def update(session:Session, id: int, datos:AlimentacionCreate ) -> Alimentacion | None:
    logger.debug(f'Comenzando actualizacion del id{id} en la tabla alimentaciones')

    consulta = session.get(Alimentacion, id)

    if not consulta:
        raise NotFoundError(Alimentacion.nombre, id)
    
    consulta.nombre = datos.nombre
    consulta.updated_at = datetime.now()
    session.add(consulta)
    session.commit()
    session.refresh(consulta)
    logger.info(f'Actualizacion existosa en el id{consulta.id} ahora con nombre {consulta.nombre}')
    return consulta

def delete(session: Session, id:int) -> bool:
    logger.debug(f'Comenzando el borrado del id{id} en la tabla alimentaciones')
    consulta = session.get(Alimentacion, id)

    if not consulta:
        raise NotFoundError(Alimentacion.nombre, id)
    
    session.delete(consulta)
    session.commit()
    return True

```

--- FILE: app/services/archivo_personal.py ---

```python
from sqlmodel import Session, select
from datetime import datetime
import logging

from sqlalchemy.exc import IntegrityError
from app.utils.errors import NotFoundError, AlreadyExistsError

from app.models.archivos_personal import ArchivosPersonal
from app.models.archivos import Archivos
from app.models.personal import Personal
from app.schemas.archivo_personal import ArchivoPersonalCreate, ArchivoPersonalRead,ArchivoPersonalUpdate


logger = logging.getLogger(__name__)


def create(datos:ArchivoPersonalCreate, session:Session)-> ArchivosPersonal:
    archivo = session.get(Archivos, datos.archivos_id)
    persona = session.get(Personal, datos.personal_id)

    if not archivo:
        raise NotFoundError(f'El archivo con id {datos.archivos_id} no existe')
    
    if not persona:
        raise NotFoundError(f'La persona con id {datos.personal_id} no existe')
    
    new_record = ArchivosPersonal(
        personal_id=datos.personal_id,
        archivos_id=datos.archivos_id,
        url=datos.url
    )
    
    session.add(new_record)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ConflictError("Esta persona ya tiene un archivo de este tipo")

    session.refresh(new_record)
    logger.info(f"ArchivoPersonal creado con id {new_record.id}")   # evento normal
    return new_record




def get_all(session: Session)-> list[ArchivosPersonal]:
    registros=select(ArchivosPersonal)
    resultado= session.exec(registros).all()
    return resultado

def get_by_personal_id(id:int, session:Session) -> list[ArchivosPersonal]:
    registros= select(ArchivosPersonal).where(ArchivosPersonal.personal_id == id)
    resultado= session.exec(registros).all()
    return resultado

def update_url(id:int, datos:ArchivoPersonalUpdate, session:Session) -> ArchivosPersonal:
    registro = session.get(ArchivosPersonal,id)

    if registro  is None:
        raise NotFoundError(f"Archivo personal con id {id} no existe")
    
    datos_registro = datos.model_dump(exclude_unset=True)   
    for campo, valor in datos_registro.items():
        setattr(registro, campo, valor)
    
    registro.updated_at = datetime.now()
    session.add(registro)
    session.commit()
    session.refresh(registro)
    return registro

def delete(id:int, session:Session)-> bool:
    registro = session.get(ArchivosPersonal,id)

    if registro is None:
        return False
    
    session.delete(registro)
    session.commit()
    return True





```

--- FILE: app/services/archivos.py ---

```python
from sqlmodel import Session, select
from datetime import datetime
import logging

from app.schemas.archivo import ArchivoCreate, ArchivoRead
from app.models.archivos import Archivos


logger = logging.getLogger(__name__)


def create(session: Session, datos:ArchivoCreate) -> ArchivoCreate:
    archivo= Archivos(nombre=datos.nombre)
    session.add(archivo)
    session.commit()
    session.refresh(archivo)
    logger.info(f'logger.info(f"ArchivoPersonal creado con id {archivo.id}") ')
    return archivo

def get_all(session: Session)-> ArchivoRead:
    consulta = select(Archivos)
    resultado = session.exec(consulta).all()
    return resultado


def get_by_id(id: int, session: Session)->ArchivoRead:
    return session.get(Archivos, id)


def update(id:int, datos:ArchivoCreate, session:Session)->ArchivoRead | None:
    archivo = session.get(Archivos, id)

    if archivo is None:
        return None
    
    archivo.nombre = datos.nombre
    archivo.updated_at = datetime.now()
    session.add(archivo)
    session.commit()
    session.refresh(archivo)
    return archivo

def delete(id: int, session: Session)-> bool:
    archivo = session.get(Archivos, id)

    if archivo is None:
        return False
    
    session.delete(archivo)
    session.commit()
    return True
```

--- FILE: app/services/banco.py ---

```python
from sqlmodel import Session, select
from datetime import datetime
from app.models.banco import Banco
from app.schemas.banco import BancoCreate


def crear_banco(session: Session, datos: BancoCreate) -> Banco:
    # 1. Convertir el schema de entrada en un objeto de la tabla
    banco = Banco(nombre=datos.nombre)
    session.add(banco)
    session.commit()
    session.refresh(banco)

    return banco


def listar_bancos(session: Session) -> list[Banco]:
    # Construye y ejecuta un SELECT * FROM bancos
    consulta = select(Banco)
    resultados = session.exec(consulta).all()
    return resultados

def obtener_banco(session: Session, banco_id: int) -> Banco | None:
    return session.get(Banco, banco_id)


def actualizar_banco(session: Session, banco_id: int, datos: BancoCreate) -> Banco | None:
    banco = session.get(Banco, banco_id)
    if banco is None:
        return None
    banco.nombre = datos.nombre
    banco.updated_at = datetime.now()
    session.add(banco)
    session.commit()
    session.refresh(banco)
    return banco


def eliminar_banco(session: Session, banco_id: int) -> bool:
    banco = session.get(Banco, banco_id)
    if banco is None:
        return False
    session.delete(banco)
    session.commit()
    return True
```

--- FILE: app/services/ciudad.py ---

```python
from sqlmodel import Session, select
from datetime import datetime

from app.models.ciudad import Ciudad
from app.schemas.ciudad import CiudadCreate, CiudadRead

def create(datos: CiudadCreate, session: Session) -> Ciudad:
    ciudad = Ciudad(nombre=datos.nombre)
    session.add(ciudad)
    session.commit()
    session.refresh(ciudad)
    return ciudad

def get_all(session:Session) -> list[CiudadRead]:
    consulta = select(Ciudad)
    resultado = session.exec(consulta).all()
    return resultado

def get_by_id(id: int, session:Session) -> CiudadRead:
    return session.get(Ciudad, id)

def update(id: int, datos:CiudadCreate, session: Session) -> CiudadCreate:
    ciudad = session.get(Ciudad, id)

    if ciudad is None:
        return None
    
    ciudad.nombre = datos.nombre
    ciudad.updated_at = datetime.now()
    session.add(ciudad)
    session.commit()
    session.refresh(ciudad)
    return ciudad

def delete(id:int, session:Session) -> bool:
    ciudad = session.get(Ciudad, id)
    
    if not ciudad:
        return False
    
    session.delete(ciudad)
    session.commit()
    return True

```

--- FILE: app/services/dato_bancario.py ---

```python
from sqlmodel import Session, select

from app.models.dato_bancario import DatoBancario
from app.models.banco import Banco
from app.models.tipo_cuenta_bancaria import TipoCuentaBancaria
from app.schemas.dato_bancario import DatoBancarioCreate


from app.utils.logger import logger
from app.utils.errors import NotFoundError, AlreadyExistsError


def crear(session: Session, data: DatoBancarioCreate) -> DatoBancario:
    logger.debug(f'Creando nueva relacion Dato bancario')

    banco = session.get(Banco, data.banco_id)
    if not banco:
        raise NotFoundError(f"El banco con id {data.banco_id} no existe")

    tipo = session.get(TipoCuentaBancaria, data.tipo_cuenta_id)
    if not tipo:
        raise NotFoundError(f"El tipo de cuenta con id {data.tipo_cuenta_id} no existe")

    cuenta = DatoBancario(
        num_cuenta=data.num_cuenta,
        banco_id=data.banco_id,
        tipo_cuenta_id=data.tipo_cuenta_id,
    )
    session.add(cuenta)
    session.commit()
    session.refresh(cuenta)
    logger.info(f'Dato bancario creado existosamente {cuenta.model_dump()}')
    return cuenta


def listar(session: Session) -> list[DatoBancario]:

    return session.exec(select(DatoBancario)).all()


def obtener(session: Session, cuenta_id: int) -> DatoBancario | None:
    return session.get(DatoBancario, cuenta_id)


def eliminar(session: Session, cuenta_id: int) -> bool:
    cuenta = session.get(DatoBancario, cuenta_id)
    if not cuenta:
        return False
    session.delete(cuenta)
    session.commit()
    return True
```

--- FILE: app/services/eps.py ---

```python
from sqlmodel import Session, select
from datetime import datetime

from app.models.eps import Eps
from app.schemas.eps import EpsCreate, EpsRead

def create(datos:EpsCreate, session:Session) -> EpsCreate:
    eps = Eps(nombre=datos.nombre)
    session.add(eps)
    session.commit()
    session.refresh(eps)
    return eps

def get_all(session:Session)->list[EpsRead]:
    eps = select(Eps)
    resultado = session.exec(eps).all()
    return resultado

def get_by_id(id: int, session: Session) -> EpsRead:
    return session.get(Eps, id)

def update(id: int, datos:EpsCreate, session:Session)->EpsRead:
    eps=session.get(Eps, id)

    if eps is None:
        return None
    
    eps.nombre = datos.nombre
    eps.updated_at = datetime.now()
    session.add(eps)
    session.commit()
    session.refresh(eps)
    return eps

def delete(id: int, session:Session)->bool:
    eps=session.get(Eps,id)


    if not eps:
        return False
    
    session.delete(eps)
    session.commit()
    return True
```

--- FILE: app/services/genero.py ---

```python
from sqlmodel import Session, select
from datetime import datetime

from app.schemas.genero import GeneroRead, GeneroCreate
from app.models.genero import Genero


def create(datos: GeneroCreate, session: Session)-> GeneroCreate:
    genero=Genero(nombre=datos.nombre)
    session.add(genero)
    session.commit()
    session.refresh(genero)
    return genero

def get_all(session: Session)->list[GeneroRead]:
    genero = select(Genero)
    resultado = session.exec(genero).all()
    return resultado

def get_by_id(id: int,session:Session)->GeneroRead:
    return session.get(Genero, id)

def update(id:int, datos:GeneroCreate, session:Session) -> GeneroRead:
    genero = session.get(Genero, id)

    if genero is None:
        return None
    
    genero.nombre = datos.nombre
    genero.updated_at = datetime.now()
    session.add(genero)
    session.commit()
    session.refresh(genero)
    return genero

def delete(id: int, session:Session):
    genero = session.get(Genero, id)

    if genero is None:
        return None
    
    session.delete(genero)
    session.commit()
    return True

```

--- FILE: app/services/personal.py ---

```python
from sqlmodel import Session, select
from datetime import datetime

from app.utils.errors import NotFoundError

from app.models import Personal, Genero, Alimentacion,Ciudad,Eps, StatusPersonal
from app.schemas.personal import PersonalCreate, PersonalRead, PersonalUpdate

def create(datos:PersonalCreate, session: Session)-> PersonalRead:
    
    if not session.get(Genero,datos.genero_id):
        raise NotFoundError(f'El genero con el id {datos.genero_id} no existe')
    if not session.get(Alimentacion, datos.alimentacion_id):
        raise NotFoundError(f'La Alimentacion con el id {datos.alimentacion_id} no existe')
    if not session.get(Ciudad, datos.ciudad_id):
        raise NotFoundError(f'La ciudad con el id {datos.ciudad_id} no existe')
    if not session.get(Eps, datos.eps_id):
        raise NotFoundError(f'La eps con el id {datos.eps_id} no existe')
    if not session.get(StatusPersonal, datos.status_personal_id):
        raise NotFoundError(f'El status personal con el id {datos.status_personal_id} no existe') 
    
    new_person = Personal(**datos.model_dump())
    session.add(new_person)
    session.commit()
    session.refresh(new_person)
    return new_person

def get_all(session: Session) -> list[Personal]:
    return session.exec(select(Personal)).all()

def get_by_id(id:int, session:Session)->PersonalRead:
    return session.get(Personal,id)

def update(id:int, datos:PersonalUpdate, session: Session)->PersonalUpdate:
    registro= session.get(Personal,id)

    if not registro:
        return None

    # Validación si FK existen (Solo si fueron enviadas en la petición)

    if datos.genero_id is not None and not session.get(Genero, datos.genero_id):
        raise NotFoundError(f"El genero con el id {datos.genero_id} no existe")

    if datos.alimentacion_id is not None and not session.get(Alimentacion, datos.alimentacion_id):
        raise NotFoundError(f"La Alimentacion con el id {datos.alimentacion_id} no existe")

    if datos.ciudad_id is not None and not session.get(Ciudad, datos.ciudad_id):
        raise NotFoundError(f"La ciudad con el id {datos.ciudad_id} no existe")

    if datos.eps_id is not None and not session.get(Eps, datos.eps_id):
        raise NotFoundError(f"La eps con el id {datos.eps_id} no existe")

    if datos.status_personal_id is not None and not session.get(StatusPersonal, datos.status_personal_id):
        raise NotFoundError(f"El status personal con el id {datos.status_personal_id} no existe")

    datos_recibidos = datos.model_dump(exclude_unset=True)
    for key, value in datos_recibidos.items():
        setattr(registro, key, value)

    
    registro.updated_at = datetime.now()
    session.add(registro)
    session.commit()
    session.refresh(registro)    
    return registro

def delete(id: int, session:Session):
    registro = session.get(Personal, id)

    if not registro:
        return False
    
    session.delete(registro)
    session.commit()
    return True

```

--- FILE: app/services/status_personal.py ---

```python
from sqlmodel import Session, select
from datetime import datetime

from app.models.status_personal import StatusPersonal
from app.schemas.status_personal import StatusPersonalCreate, StatusPersonalRead

def create(datos: StatusPersonalCreate, session: Session) -> StatusPersonalRead:
    status= StatusPersonal(nombre=datos.nombre)
    session.add(status)
    session.commit()
    session.refresh(status)
    return status

def get_all(session: Session)->StatusPersonalRead:
    status = select(StatusPersonal)
    resultado = session.exec(status).all()
    return resultado

def get_by_id(id: int, session: Session)-> StatusPersonalRead:
    status = session.get(StatusPersonal, id)

    if status is None:
        return None
    
    return status

def update(id: int, datos: StatusPersonalCreate, session:Session)-> StatusPersonalRead:
    status = session.get(StatusPersonal, id)

    if status is None:
        return None
    
    status.nombre = datos.nombre
    status.updated_at = datetime.now()
    session.add(status)
    session.commit()
    session.refresh(status)
    return status

def delete(id: int, session:Session)-> bool:
    status = session.get(StatusPersonal, id)

    if status is None:
        return False
    
    session.delete(status)
    session.commit()
    return True

```

--- FILE: app/services/tipo_cuenta_bancaria.py ---

```python
from sqlmodel import Session, select
from app.models.tipo_cuenta_bancaria import TipoCuentaBancaria
from app.schemas.tipo_cuenta_bancaria import TipoCuentaCreate
from datetime import datetime

def crear(session: Session, data: TipoCuentaCreate) -> TipoCuentaBancaria:
    tipo = TipoCuentaBancaria(nombre=data.nombre)
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo


def listar(session: Session) -> list[TipoCuentaBancaria]:
    return session.exec(select(TipoCuentaBancaria)).all()


def obtener(session: Session, tipo_id: int) -> TipoCuentaBancaria | None:
    return session.get(TipoCuentaBancaria, tipo_id)


def actualizar(session: Session, tipo_id: int, data: TipoCuentaCreate) -> TipoCuentaBancaria | None:
    tipo = session.get(TipoCuentaBancaria, tipo_id)
    if not tipo:
        return None
    tipo.nombre = data.nombre
    tipo.updated_at = datetime.now()
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo


def eliminar(session: Session, tipo_id: int) -> bool:
    tipo = session.get(TipoCuentaBancaria, tipo_id)
    if not tipo:
        return False
    session.delete(tipo)
    session.commit()
    return True


```

--- FILE: app/utils/__init__.py ---

```python

```

--- FILE: app/utils/errors.py ---

```python

class NotFoundError(Exception):
    def __init__(self,entity:str, id: int = None):
        self.id = id
        self.entity = entity
        message = f'El {entity.name} con el id {id} no se encontro' if id else f'ID {id} no existe'
        super().__init__(message)

class AlreadyExistsError(Exception):
    def __init__(self,entity: str, field: str, value: str):
        self.entity = entity
        self.field = field
        self.value = value
        message = f'{entity} con {field}={value} ya existe'
        super().__init__(message)

class BussinesError(Exception):
    def __init__(self, message: str):
        super().__init__(message) 

class DatabaseError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
```

--- FILE: app/utils/handlers.py ---

```python
from fastapi import Request
from fastapi.responses import JSONResponse

from app.utils.errors import NotFoundError, AlreadyExistsError, BussinesError, DatabaseError
from app.utils.logger import logger


async def not_found_handler(request: Request, exc: NotFoundError):
    logger.warning(f'NOT FOUND | {exc} | {request.method} {request.url}')
    return JSONResponse(
        status_code=404,
        content={
            'error': 'not_found',
            'message': str(exc)
        }
    )

async def already_exists_handler(request: Request, exc:AlreadyExistsError):
    logger.warning(f'CONFLICTO | {exc} | {request.method} {request.url}')
    return JSONResponse(
        status_code=409,
        content={
            'error': 'Ya existe',
            'message': str(exc)
        }
    )


async def bussines_error_handler(request: Request, exc: BussinesError):
    logger.error(f'ERROR | {exc} | {request.method} {request.url}')
    return JSONResponse(
        status_code= 422,
        content={
            'error': 'business_error',
            'message': str(exc)
        }
    )

async def database_error_handler(request: Request, exc: DatabaseError):
    logger.error(f'DATABASE ERROR |  {exc} | {request.method} {request.url}')
    return JSONResponse(
        status_code=500,
        content={
            'error': 'database_error',
            'message': str(exc)
        }
    )



```

--- FILE: app/utils/logger.py ---

```python
from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    format= '<level>{time:YYYY:MM:DD}</level> | <level>{level:<8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <cyan>{message}</cyan>',
    level= 'DEBUG',
    colorize= True
)

logger.add(
    'logs/app.logs',
    format= '{time:YYYY:MM:DD HH:mm:ss} | {level:<8} | {name}:{function}:{line} | {message}',
    level= 'INFO',
    rotation='1 day',
    retention='7 days',
    encoding='utf-8'
)

__all__=['logger']
```
