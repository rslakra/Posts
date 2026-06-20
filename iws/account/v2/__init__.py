#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

bp = APIRouter(prefix="/accounts", tags=["Accounts v2"])

from account import routes  # noqa: E402,F401
