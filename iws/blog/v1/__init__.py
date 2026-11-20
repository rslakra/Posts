#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

blog_router = APIRouter(prefix="/blogs", tags=["Blogs v1"])

from blog import routes  # noqa: E402,F401
