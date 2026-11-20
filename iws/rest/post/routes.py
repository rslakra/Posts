#
# Author: Rohtash Lakra
#
import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from rest.base import BaseRouter
from rest.post.schema import PostSchema
from rest.post.v1 import bp as bp_post_v1

logger = logging.getLogger(__name__)


class PostRouter(BaseRouter):
    """PostRouter handles post endpoints."""

    async def create(self, request: Request):
        """Create a post payload placeholder response."""
        logger.debug(f"+create() => request={request}, args={request.query_params}")
        role = None
        body = await self.json_or_none(request)
        if isinstance(body, dict):
            name = body.get("name", None)
            active = body.get("active", False)
            role = PostSchema.create(name=name, active=active)

        return JSONResponse(status_code=200, content={"status": 200, "data": role})

    async def get(self, request: Request):
        """Fetch posts placeholder response."""
        logger.debug(f"+get() => request={request}, args={request.query_params}")
        return JSONResponse(status_code=200, content={"status": 200, "data": []})


postRouter = PostRouter()
bp_post_v1.add_api_route("/", postRouter.create, methods=["POST"])
bp_post_v1.add_api_route("/", postRouter.get, methods=["GET"])
