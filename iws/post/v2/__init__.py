#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

bp = APIRouter(prefix="/posts", tags=["Posts v2"])

from post import routes  # noqa: E402,F401
