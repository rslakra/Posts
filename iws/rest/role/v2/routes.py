#
# Author: Rohtash Lakra
#
import logging

from flask import request, make_response

from framework.http import HTTPStatus
from framework.orm.pydantic.model import ResponseModel
from rest.role.model import Role
from rest.role.v2 import bp as bp_v2_role

logger = logging.getLogger(__name__)


@bp_v2_role.get("/v2-route")
def v2_route():
    logger.debug(f"v2_route => {request}")
    response = ResponseModel.buildResponse(HTTPStatus.OK)
    response.addInstance(Role("v2-route-role1", True))
    response.addInstance(Role("v2-route-role2", False))
    response.addInstance(Role("v2-route-role3", True))
    logger.debug(f"response={response}")
    return make_response(response.to_json(), response.status)
