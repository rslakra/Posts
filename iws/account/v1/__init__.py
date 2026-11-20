#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

account_router = APIRouter(prefix="/accounts", tags=["Accounts v1"])

from account import routes  # noqa: E402,F401
