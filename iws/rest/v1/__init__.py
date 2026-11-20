#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

from rest.company.v1 import bp as company_v1_bp
from rest.contact.v1 import bp as contact_v1_bp
from rest.post.v1 import bp as post_v1_bp
from rest.role.permission_routes import bp as permission_bp
from rest.role.v1 import bp as role_v1_bp
from rest.user.v1 import bp as user_v1_bp

bp = APIRouter(prefix="/v1")
"""
Versioned Router Notes (`v1`):

This router groups all version-1 REST resources under `/v1`.
Each resource router contributes its own prefix (for example `/users`, `/roles`),
and FastAPI composes them into the final paths.

Example:
- parent prefix: `/rest`
- version prefix: `/v1`
- resource prefix: `/users`
- final route prefix: `/rest/v1/users`
"""

# Register REST APIs (end-points) here
bp.include_router(role_v1_bp)
bp.include_router(permission_bp)
bp.include_router(user_v1_bp)
bp.include_router(company_v1_bp)
bp.include_router(contact_v1_bp)
bp.include_router(post_v1_bp)
