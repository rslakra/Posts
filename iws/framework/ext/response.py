#
# Author: Rohtash Lakra
#
from werkzeug.wrappers.response import Response


class JsonResponse(Response):
    """Custom JSON Response"""

    # set default mime-type of all requests.
    default_mimetype = "application/json; charset=utf-8"

    # @classmethod
    # def force_type(cls, response, environ=None):
    #     """Enforce that the WSGI response is a response object of the current type."""
    #     if isinstance(response, dict):
    #         response = jsonify(response)
    #
    #     return super(JsonResponse, cls).force_type(response, environ)
