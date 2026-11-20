#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

bp = APIRouter(prefix="/contacts")

from rest.contact import routes  # noqa: E402,F401
