#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

from api.v1 import bp as api_v1_bp
from api.v2 import bp as api_v2_bp

bp = APIRouter(prefix="/api")
"""
FastAPI Router Notes:

`APIRouter` groups related end-points (it replaces Flask's `Blueprint`).

Common constructor arguments:
- `prefix`: prepends a path segment to all routes of this router.
- `tags`: groups routes in the OpenAPI/Swagger docs.
- `dependencies`: applies shared dependencies to all routes.
- `responses`: defines shared response metadata for all routes.

An `APIRouter` is not an application. It must be registered with `include_router()` on the FastAPI app (or another
router) before its end-points become active.
"""

# register versioned end-points here (final paths: /api/v1/..., /api/v2/...)
bp.include_router(api_v1_bp)
bp.include_router(api_v2_bp)
