from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.db.session import init_db
from app.models.banco import Banco  # importar para que SQLModel lo registre
from app.api.hub import api_hub


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que corre al ARRANCAR la app
    print("Iniciando aplicación: creando tablas...")
    init_db()
    yield
    # Código que corre al APAGAR la app
    print("Apagando aplicación...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.include_router(api_hub)

@app.get("/")
def raiz():
    return {"mensaje": "API del formulario funcionando", "version": settings.VERSION}