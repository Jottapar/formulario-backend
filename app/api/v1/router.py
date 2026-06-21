from fastapi import APIRouter

from app.api.v1.endpoints import bancos

router_v1 = APIRouter()

router_v1.include_router(bancos.router)