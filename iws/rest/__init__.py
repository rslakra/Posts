#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

from rest.v1 import bp as rest_v1_bp
from rest.v2 import bp as rest_v2_bp

bp = APIRouter(prefix="/rest")
"""
FastAPI Router Notes:

`APIRouter` in FastAPI is similar to Flask `Blueprint` for organizing endpoints.

Common constructor arguments:
- `prefix`: prepends a path segment to all routes in this router.
- `tags`: groups routes in OpenAPI/Swagger docs.
- `dependencies`: applies shared dependencies to all routes.
- `responses`: defines shared response metadata for all routes.

`APIRouter` is not a standalone application. You must register it on the FastAPI app
or on another router using `include_router()` so its endpoints become active.
"""

# Register REST API paths here.
bp.include_router(rest_v1_bp)
bp.include_router(rest_v2_bp)
