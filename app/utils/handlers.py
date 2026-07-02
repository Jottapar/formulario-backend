from fastapi import Request
from fastapi.responses import JSONResponse

from app.utils.exceptions import NotFoundError, ConflictError, BusinessError

async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


async def conflict_handler(request: Request, exc: ConflictError) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )


async def business_error_handler(request: Request, exc: BusinessError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )