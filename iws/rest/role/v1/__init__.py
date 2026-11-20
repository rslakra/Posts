#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

bp = APIRouter(prefix="/roles")

from rest.role import routes  # noqa: E402,F401
