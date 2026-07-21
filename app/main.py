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