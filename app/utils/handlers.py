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


