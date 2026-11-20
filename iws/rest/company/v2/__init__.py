#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

bp = APIRouter(prefix="/companies")

from rest.company import routes  # noqa: E402,F401
