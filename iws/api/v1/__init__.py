#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

from admin.v1 import admin_router
from account.v1 import account_router
from post.v1 import post_router
from blog.v1 import blog_router
from comment.v1 import comment_router

bp = APIRouter(prefix="/v1")
"""
Version 1 router. Each feature router contributes its own prefix (e.g. `/accounts`), so the final paths look like
`/api/v1/accounts/...`.

The same feature routers are also served by the web application (`webapp.routes`) and documented there, so they are
excluded from the OpenAPI schema here to avoid duplicated operations.
"""

# register end-points here
bp.include_router(admin_router, include_in_schema=False)
bp.include_router(account_router, include_in_schema=False)
bp.include_router(post_router, include_in_schema=False)
bp.include_router(blog_router, include_in_schema=False)
bp.include_router(comment_router, include_in_schema=False)
