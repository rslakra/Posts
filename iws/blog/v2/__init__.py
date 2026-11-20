#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

bp = APIRouter(prefix="/blogs", tags=["Blogs v2"])

from blog import routes  # noqa: E402,F401
