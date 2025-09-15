#
# Author: Rohtash Lakra
#
import logging

from flask import request, make_response

from framework.http import HTTPStatus
from framework.orm.pydantic.model import ResponseModel
from rest.company.model import Company
from rest.company.v1 import bp as bp_v1_role

logger = logging.getLogger(__name__)


@bp_v1_role.get("/v1-route")
def v1_route():
    logger.debug(f"v1_route => {request}")
    response = ResponseModel.buildResponse(HTTPStatus.OK)
    response.addInstance(Company("v1-route-role1", False))
    response.addInstance(Company("v1-route-role2", True))
    response.addInstance(Company("v1-route-role3", False))
    logger.debug(f"response={response}")
    return make_response(response.to_json(), response.status)
