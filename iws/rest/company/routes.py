#
# Author: Rohtash Lakra
#
import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from rest.base import BaseRouter
from framework.exception.duplicate import DuplicateRecordException
from framework.exception.not_found import NoRecordFoundException
from framework.exception.validation import ValidationException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import ResponseModel
from framework.orm.sqlalchemy.schema import SchemaOperation
from rest.company.model import Company
from rest.company.service import CompanyService
from rest.company.v1 import bp as bp_company_v1

logger = logging.getLogger(__name__)


class CompanyRouter(BaseRouter):
    """CompanyRouter handles CRUD operations for company resources."""

    async def create(self, request: Request):
        """Create a company."""
        logger.debug(f"+create() => request={request}, args={request.query_params}")
        try:
            body = await self.json_or_none(request)
            company = None
            if body is not None:
                logger.debug(f"body={body}")
                company = Company(**body)
                logger.debug(f"company={company}")

            companyService = CompanyService()
            companyService.validate(SchemaOperation.CREATE, company)
            company = companyService.create(company)
            logger.debug(f"company={company}")
            response = ResponseModel(status=HTTPStatus.CREATED.statusCode, message="Company is successfully created.")
            response.addInstance(company)
        except ValidationException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except DuplicateRecordException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-create() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def bulkCreate(self, request: Request):
        """Create multiple companies in one request."""
        logger.debug(f"+bulkCreate() => request={request}, args={request.query_params}")
        try:
            companies = []
            body = await self.json_or_none(request)
            if body is not None:
                logger.debug(f"type={type(body)}, body={body}")
                if isinstance(body, list):
                    companies = [Company(**entry) for entry in body]
                elif isinstance(body, dict):
                    companies.append(Company(**body))

            logger.debug(f"companies={companies}")
            companyService = CompanyService()
            companyService.validates(SchemaOperation.CREATE, companies)
            companies = companyService.bulkCreate(companies)
            logger.debug(f"companies={companies}")
            response = ResponseModel(status=HTTPStatus.CREATED.statusCode, message="Companys are successfully created.")
            response.addInstances(companies)
        except ValidationException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except DuplicateRecordException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-bulkCreate() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def get(self, request: Request):
        """Fetch companies using optional query filters."""
        logger.debug(f"+get() => request={request}, args={request.query_params}")
        try:
            companyService = CompanyService()
            companies = companyService.findByFilter(self.query_params(request))
            response = ResponseModel.buildResponse(HTTPStatus.OK)
            if companies:
                response.addInstances(companies)
            else:
                response.message = "No Records Exist!"
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-get() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def update(self, request: Request):
        """Update an existing company."""
        logger.debug(f"+update() => request={request}, args={request.query_params}")
        try:
            body = await self.json_or_none(request)
            company = None
            if body is not None:
                logger.debug(f"body={body}")
                company = Company(**body)
                logger.debug(f"company={company}")

            companyService = CompanyService()
            companyService.validate(SchemaOperation.UPDATE, company)
            company = companyService.update(company)
            logger.debug(f"company={company}")
            response = ResponseModel(status=HTTPStatus.OK.statusCode, message="Company is successfully updated.")
            response.addInstance(company)
        except ValidationException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except NoRecordFoundException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-update() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def delete(self, id: int, request: Request):
        """Delete a company by id."""
        logger.debug(f"+delete({id}) => request={request}, args={request.query_params}")
        try:
            body = await self.json_or_none(request)
            if body is not None:
                logger.debug(f"body={body}")
                company = Company(**body)
                logger.debug(f"company={company}")

            companyService = CompanyService()
            companyService.delete(id)
            response = ResponseModel(status=HTTPStatus.OK.statusCode, message="Company is successfully deleted.")
        except NoRecordFoundException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-delete() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())


companyRouter = CompanyRouter()
bp_company_v1.add_api_route("/", companyRouter.create, methods=["POST"])
bp_company_v1.add_api_route("/batch", companyRouter.bulkCreate, methods=["POST"])
bp_company_v1.add_api_route("/", companyRouter.get, methods=["GET"])
bp_company_v1.add_api_route("/", companyRouter.update, methods=["PUT"])
bp_company_v1.add_api_route("/{id}", companyRouter.delete, methods=["DELETE"])
