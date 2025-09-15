#
# Author: Rohtash Lakra
#
import logging

from flask import request, make_response

from framework.http import HTTPStatus
from framework.orm.pydantic.model import ResponseModel
from rest.company.model import Company
from rest.company.v2 import bp as bp_v2_company

logger = logging.getLogger(__name__)


@bp_v2_company.get("/v2-route")
def v2_route():
    logger.debug(f"v2_route => {request}")
    response = ResponseModel.buildResponse(HTTPStatus.OK)
    response.addInstance(Company("v2-route-company1", True))
    response.addInstance(Company("v2-route-company2", False))
    response.addInstance(Company("v2-route-company3", True))
    logger.debug(f"response={response}")
    return make_response(response.to_json(), response.status)
