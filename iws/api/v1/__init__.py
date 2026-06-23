#
# Author: Rohtash Lakra
#
from flask import Blueprint
from admin.v1 import admin_router
from account.v1 import account_router
from post.v1 import post_router
from blog.v1 import blog_router
from comment.v1 import comment_router

bp = Blueprint("v1", __name__, url_prefix="/v1")
"""
Create an instance of Blueprint prefixed with '/bp' as named bp.
Parameters:
    name: represents the name of the blueprint, which Flask’s routing mechanism uses and identifies it in the project.
    __name__: The Blueprint’s import name, which Flask uses to locate the Blueprint’s resources.
    url_prefix: the path to prepend to all of the Blueprint’s URLs.
"""


# register end-points here
bp.register_blueprint(admin_router)
bp.register_blueprint(account_router)
bp.register_blueprint(post_router)
bp.register_blueprint(blog_router)
bp.register_blueprint(comment_router)
