#
# Author: Rohtash Lakra
#
from flask import Blueprint

from rest.company.v2 import bp as company_v2_bp
from rest.contact.v2 import bp as contact_v2_bp
from rest.post.v2 import bp as post_v2_bp
from rest.role.v2 import bp as role_v2_bp
from rest.user.v2 import bp as user_v2_bp

bp = Blueprint("v2", __name__, url_prefix="/v2")
"""
Create an instance of Blueprint prefixed with '/bp' as named bp.
Parameters:
    name: represents the name of the blueprint, which Flask’s routing mechanism uses and identifies it in the project.
    __name__: The Blueprint’s import name, which Flask uses to locate the Blueprint’s resources.
    url_prefix: the path to prepend to all of the Blueprint’s URLs.
"""

# Register REST APIs (end-points) here
bp.register_blueprint(role_v2_bp)
bp.register_blueprint(user_v2_bp)
bp.register_blueprint(company_v2_bp)
bp.register_blueprint(contact_v2_bp)
bp.register_blueprint(post_v2_bp)
