from fastapi import APIRouter

from app.api.v1.router import router_v1
from app.core.config import settings

api_hub = APIRouter()

api_hub.include_router(router_v1, prefix=settings.API_V1_STR)