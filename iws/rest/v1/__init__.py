#
# Author: Rohtash Lakra
#
from flask import Blueprint

from rest.company.v1 import bp as company_v1_bp
from rest.contact.v1 import bp as contact_v1_bp
from rest.post.v1 import bp as post_v1_bp
from rest.role.permission_routes import bp as permission_bp
from rest.role.v1 import bp as role_v1_bp
from rest.user.v1 import bp as user_v1_bp

bp = Blueprint("v1", __name__, url_prefix="/v1")
"""
Create an instance of Blueprint prefixed with '/bp' as named bp.
Parameters:
    name: represents the name of the blueprint, which Flask’s routing mechanism uses and identifies it in the project.
    __name__: The Blueprint’s import name, which Flask uses to locate the Blueprint’s resources.
    url_prefix: the path to prepend to all of the Blueprint’s URLs.
"""

# Register REST APIs (end-points) here
bp.register_blueprint(role_v1_bp)
bp.register_blueprint(permission_bp)
bp.register_blueprint(user_v1_bp)
bp.register_blueprint(company_v1_bp)
bp.register_blueprint(contact_v1_bp)
bp.register_blueprint(post_v1_bp)
