import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from app.utils.exceptions import NotFoundError, ConflictError, BusinessError

logger = logging.getLogger(__name__)


async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    logger.warning(f"NotFound en {request.url.path}: {exc}")
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


async def conflict_handler(request: Request, exc: ConflictError) -> JSONResponse:
    logger.warning(f"Conflict en {request.url.path}: {exc}")
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )


async def business_error_handler(request: Request, exc: BusinessError) -> JSONResponse:
    logger.error(f"BusinessError en {request.url.path}: {exc}")
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )