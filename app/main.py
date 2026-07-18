from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings

from app.utils.logging_config import setup_logging


from app.api.hub import api_hub
from app.utils.handlers import not_found_handler, conflict_handler, business_error_handler
from app.utils.exceptions import NotFoundError, ConflictError, BusinessError



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
app.add_exception_handler(ConflictError, conflict_handler)
app.add_exception_handler(BusinessError, business_error_handler)

app.include_router(api_hub)



@app.get("/")
def raiz():
    return {"mensaje": "API del formulario funcionando", "version": settings.VERSION}