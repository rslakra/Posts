#
# Author: Rohtash Lakra
# References:
# - https://realpython.com/flask-blueprint/
# - https://flask.palletsprojects.com/en/2.3.x/tutorial/views/#require-authentication-in-other-views
#
import logging

from flask import make_response, request

from framework.exception import DuplicateRecordException, ValidationException, RecordNotFoundException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import ResponseModel
from framework.orm.sqlalchemy.schema import SchemaOperation
from rest.company.model import Company
from rest.company.service import CompanyService
from rest.company.v1 import bp as bp_company_v1

logger = logging.getLogger(__name__)


@bp_company_v1.post("/")
def create():
    logger.debug(f"+create() => request={request}, args={request.args}, is_json:{request.is_json}")
    # post_data = request.form.to_dict(flat=False)
    try:
        if request.is_json:
            body = request.get_json()
            logger.debug(f"body={body}")
            company = Company(**body)
            logger.debug(f"company={company}")

        companyService = CompanyService()
        companyService.validate(SchemaOperation.CREATE, company)
        company = companyService.create(company)
        logger.debug(f"company={company}")
        # build success response
        response = ResponseModel(status=HTTPStatus.CREATED.statusCode, message="Company is successfully created.")
        response.addInstance(company)
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except DuplicateRecordException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-create() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_company_v1.post("/batch")
def bulkCreate():
    logger.debug(f"+bulkCreate() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        companies = []
        if request.is_json:
            body = request.get_json()
            logger.debug(f"type={type(body)}, body={body}")

            if isinstance(body, list):
                companies = [Company(**entry) for entry in body]
            elif isinstance(body, dict):
                companies.append(Company(**body))
            else:
                # handle form fields here.
                body = request.form.to_dict()
                companies.append(Company(**body))

        logger.debug(f"companies={companies}")
        companyService = CompanyService()
        companyService.validates(SchemaOperation.CREATE, companies)
        companies = companyService.bulkCreate(companies)
        logger.debug(f"companies={companies}")
        # build success response
        response = ResponseModel(status=HTTPStatus.CREATED.statusCode, message="Companys are successfully created.")
        response.addInstances(companies)
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except DuplicateRecordException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-bulkCreate() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_company_v1.get("/")
def get():
    logger.debug(f"+get() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        companyService = CompanyService()
        # if len(request.args) == 1:
        #     return companyService.findById(request.args.get('id'))
        # else:
        #     companies = companyService.findByFilter(request.args)
        companies = companyService.findByFilter(request.args)

        # build success response
        response = ResponseModel.buildResponse(HTTPStatus.OK)
        if companies:
            response.addInstances(companies)
        else:
            response.message = "No Records Exist!"
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-get() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_company_v1.put("/")
def update():
    logger.debug(f"+update() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        if request.is_json:
            body = request.get_json()
            logger.debug(f"body={body}")
            company = Company(**body)
            logger.debug(f"company={company}")

        companyService = CompanyService()
        companyService.validate(SchemaOperation.UPDATE, company)
        company = companyService.update(company)
        logger.debug(f"company={company}")

        # build success response
        response = ResponseModel(status=HTTPStatus.OK.statusCode, message="Company is successfully updated.")
        response.addInstance(company)
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except RecordNotFoundException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-update() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_company_v1.delete("/<id>")
def delete(id: int):
    logger.debug(f"+delete({id}) => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        if request.is_json:
            body = request.get_json()
            logger.debug(f"body={body}")
            company = Company(**body)
            logger.debug(f"company={company}")

        companyService = CompanyService()
        companyService.delete(id)
        # build success response
        response = ResponseModel(status=HTTPStatus.OK.statusCode, message="Company is successfully deleted.")
    except RecordNotFoundException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except RecordNotFoundException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-delete() <= response={response}")
    return make_response(response.to_json(), response.status)
