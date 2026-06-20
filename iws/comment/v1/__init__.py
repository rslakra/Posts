#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

comment_router = APIRouter(prefix="/comments", tags=["Comments v1"])

from comment import routes  # noqa: E402,F401
