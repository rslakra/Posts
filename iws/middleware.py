#
# Author: Rohtash Lakra
#
import uuid

from contextvars import ContextVar
from starlette.types import (
    ASGIApp,
    Receive,
    Send,
)
from starlette.types import Scope

REQUEST_ID_KEY = "request_id"

_context_request_id: ContextVar[str] = ContextVar(REQUEST_ID_KEY, default=None)


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

# app.add_middleware(RequestIDMiddleware)
