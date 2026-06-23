#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

bp = APIRouter(prefix="/posts")

from rest.post import routes  # noqa: E402,F401
