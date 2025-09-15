#
# Author: Rohtash Lakra
#
from flask import Blueprint
from admin.v2 import bp as admin_v2_bp
from account.v2 import bp as account_v2_bp
from post.v2 import bp as post_v2_bp
from blog.v2 import bp as blog_v2_bp
from comment.v2 import bp as comment_v2_bp

bp = Blueprint("v2", __name__, url_prefix="/v2")
"""
Create an instance of Blueprint prefixed with '/bp' as named bp.
Parameters:
    name: represents the name of the blueprint, which Flask’s routing mechanism uses and identifies it in the project.
    __name__: The Blueprint’s import name, which Flask uses to locate the Blueprint’s resources.
    url_prefix: the path to prepend to all of the Blueprint’s URLs.
"""


# register end-points here
bp.register_blueprint(admin_v2_bp)
bp.register_blueprint(account_v2_bp)
bp.register_blueprint(post_v2_bp)
bp.register_blueprint(blog_v2_bp)
bp.register_blueprint(comment_v2_bp)
