#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

from rest.company.v2 import bp as company_v2_bp
from rest.contact.v2 import bp as contact_v2_bp
from rest.post.v2 import bp as post_v2_bp
from rest.role.v2 import bp as role_v2_bp
from rest.user.v2 import bp as user_v2_bp

bp = APIRouter(prefix="/v2")
"""
Versioned Router Notes (`v2`):

This router groups all version-2 REST resources under `/v2`.
Routers are mounted with `include_router()`, and their prefixes are combined
to build final endpoint paths.

Example final prefix pattern:
`/rest` + `/v2` + `/resource`
"""

# Register REST APIs (end-points) here
bp.include_router(role_v2_bp)
bp.include_router(user_v2_bp)
bp.include_router(company_v2_bp)
bp.include_router(contact_v2_bp)
bp.include_router(post_v2_bp)
