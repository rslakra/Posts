#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

bp = APIRouter(prefix="/comments", tags=["Comments v2"])

from comment import routes  # noqa: E402,F401
