#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

bp = APIRouter(prefix="/admin", tags=["Admin v2"])

from admin import routes  # noqa: E402,F401
