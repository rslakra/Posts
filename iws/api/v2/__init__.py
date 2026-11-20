#
# Author: Rohtash Lakra
#
from fastapi import APIRouter

from admin.v2 import bp as admin_v2_bp
from account.v2 import bp as account_v2_bp
from post.v2 import bp as post_v2_bp
from blog.v2 import bp as blog_v2_bp
from comment.v2 import bp as comment_v2_bp

bp = APIRouter(prefix="/v2")
"""
Version 2 router. Each feature router contributes its own prefix (e.g. `/accounts`), so the final paths look like
`/api/v2/accounts/...`.
"""

# register end-points here
bp.include_router(admin_v2_bp)
bp.include_router(account_v2_bp)
bp.include_router(post_v2_bp)
bp.include_router(blog_v2_bp)
bp.include_router(comment_v2_bp)
