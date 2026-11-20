#
# Author: Rohtash Lakra
#
from fastapi.responses import JSONResponse


class JsonResponse(JSONResponse):
    """Custom JSON Response"""

    # set default mime-type of all requests.
    media_type = "application/json; charset=utf-8"
