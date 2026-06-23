#
# Author: Rohtash Lakra
#
import logging
import time
import uuid

from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import AsyncIterator

from fastapi import FastAPI, Request
from sqlalchemy import text
from starlette.types import (
    ASGIApp,
    Receive,
    Send,
)
from starlette.types import Scope
from starlette.responses import Response

from globals import connector

REQUEST_ID_KEY = "request_id"

_context_request_id: ContextVar[str] = ContextVar(REQUEST_ID_KEY, default=None)
logger = logging.getLogger(__name__)


def get_request_id() -> str:
    return _context_request_id.get()


class RequestIDMiddleware:
    def __init__(
            self,
            app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        request_id = _context_request_id.set(uuid.uuid4().hex)
        await self.app(scope, receive, send)

        _context_request_id.reset(request_id)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # pylint: disable=redefined-outer-name
    """Application startup/shutdown lifecycle hooks."""
    print("Startup")
    logger.info("Startup")
    logger.info("Validating DB connection on startup...")
    # Connector uses sync SQLAlchemy Session/Engine APIs, so probe with sync connection.
    with connector.engine.connect() as db_conn:
        db_conn.execute(text("SELECT 1"))
    logger.info("Database connection validated during startup.")
    yield

    if connector.engine is not None:  # pylint: disable=protected-access
        connector.engine.dispose()
        logger.info("Database engine disposed on shutdown.")

    logger.info("Shutdown")
    print("Shutdown")


async def add_process_time_header(request: Request, next_call) -> Response:
    """HTTP middleware to log request/response and add process-time header."""
    logger.info(
        "request.start method=%s path=%s content_type=%s",
        request.method,
        request.url.path,
        request.headers.get("content-type"),
    )
    start_time = time.time()
    response = await next_call(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    if response.status_code == 405:
        logger.warning(
            "request.method_not_allowed method=%s path=%s allow=%s",
            request.method,
            request.url.path,
            response.headers.get("allow"),
        )
    logger.info(
        "request.end method=%s path=%s status=%s process_time=%.6f",
        request.method,
        request.url.path,
        response.status_code,
        process_time,
    )
    return response
