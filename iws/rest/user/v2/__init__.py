#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

bp = APIRouter(prefix="/users")

from rest.user import routes  # noqa: E402,F401
