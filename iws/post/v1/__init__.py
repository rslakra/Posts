#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

post_router = APIRouter(prefix="/posts", tags=["Posts v1"])

from post import routes  # noqa: E402,F401
