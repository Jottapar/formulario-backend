from fastapi import APIRouter

from app.api.v1.endpoints import bancos, tipo_cuenta_bancaria, dato_bancario, alimentacion, archivos

router_v1 = APIRouter()

router_v1.include_router(bancos.router)
router_v1.include_router(tipo_cuenta_bancaria.router)
router_v1.include_router(dato_bancario.router)
router_v1.include_router(alimentacion.router)
router_v1.include_router(archivos.router)