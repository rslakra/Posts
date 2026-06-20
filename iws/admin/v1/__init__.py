#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

admin_router = APIRouter(prefix="/admin", tags=["Admin v1"])

from admin import routes  # noqa: E402,F401
