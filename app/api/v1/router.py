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