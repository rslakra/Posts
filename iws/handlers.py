#
# Author: Rohtash Lakra
#
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from framework.exception.abstract import AbstractException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import ErrorModel

logger = logging.getLogger(__name__)


def _errorResponse(statusCode: int, message: str) -> JSONResponse:
    """Builds the JSON error response (same shape as the ErrorModel used by the rest of the application)."""
    error = ErrorModel(status=statusCode, message=message)
    return JSONResponse(status_code=statusCode, content=error.model_dump(mode="json", exclude_none=True))


async def httpExceptionHandler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handles HTTP errors (400, 404, 405 ...), replaces the Flask 'errorhandler' for the HTTP errors."""
    logger.error(f"HTTP error, method={request.method}, path={request.url.path}, status={exc.status_code}, error={exc}")
    return _errorResponse(exc.status_code, str(exc.detail))


async def validationExceptionHandler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handles the request validation errors of FastAPI."""
    message = "; ".join(
        f"{'.'.join(str(part) for part in error.get('loc', ()))}: {error.get('msg')}" for error in exc.errors()
    )
    logger.error(f"Validation error, method={request.method}, path={request.url.path}, error={message}")
    return _errorResponse(HTTPStatus.INVALID_DATA.statusCode, message)


async def abstractExceptionHandler(request: Request, exc: AbstractException) -> JSONResponse:
    """Handles the application's exceptions (validation, duplicate, not-found, authentication ...)."""
    httpStatus = exc.httpStatus or HTTPStatus.INTERNAL_SERVER_ERROR
    message = "; ".join(str(message) for message in (exc.messages or []) if message) or httpStatus.message
    logger.error(f"{type(exc).__name__}, method={request.method}, path={request.url.path}, error={message}")
    return _errorResponse(httpStatus.statusCode, message)


async def unhandledExceptionHandler(request: Request, exc: Exception) -> JSONResponse:
    """Handles any other error as '500 - Internal Server Error' without leaking the details to the client."""
    logger.error(f"Unhandled error, method={request.method}, path={request.url.path}", exc_info=exc)
    return _errorResponse(HTTPStatus.INTERNAL_SERVER_ERROR.statusCode, HTTPStatus.INTERNAL_SERVER_ERROR.message)


def registerExceptionHandlers(app: FastAPI) -> None:
    """Registers the application's exception handlers."""
    app.add_exception_handler(StarletteHTTPException, httpExceptionHandler)
    app.add_exception_handler(RequestValidationError, validationExceptionHandler)
    app.add_exception_handler(AbstractException, abstractExceptionHandler)
    app.add_exception_handler(Exception, unhandledExceptionHandler)
