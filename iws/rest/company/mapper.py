#
# Author: Rohtash Lakra
#
import logging

from framework.orm.mapper import Mapper
from framework.orm.pydantic.model import BaseModel
from framework.orm.sqlalchemy.schema import BaseSchema
from rest.company.model import Company
from rest.company.schema import CompanySchema

logger = logging.getLogger(__name__)


class CompanyMapper(Mapper):

    @classmethod
    # @override
    def fromSchema(self, companySchema: CompanySchema) -> Company:
        logger.debug(f"+fromSchema({companySchema})")
        company = Company(**companySchema.toJSONObject())
        if companySchema.branches:
            company.branches = [Company(**branch.toJSONObject()) for branch in companySchema.branches]
            logger.debug(f"company.branches={company.branches}")

        logger.debug(f"-fromSchema(), company={company}")
        return company

    @classmethod
    # @override
    def fromModel(self, company: Company) -> CompanySchema:
        logger.debug(f"+fromModel({company})")
        companySchema = CompanySchema(**company.toJSONObject())
        if company.branches:
            companySchema.branches = [CompanySchema(**branch.toJSONObject()) for branch in company.branches]
            logger.debug(f"companySchema.branches={companySchema.branches}")

        logger.debug(f"-fromModel(), companySchema={companySchema}")
        return companySchema

    @classmethod
    def fromSchemas(cls, schemaObjects: list[BaseSchema]) -> list[BaseModel]:
        return [CompanyMapper.fromSchema(schemaObject) for schemaObject in schemaObjects]

    @classmethod
    def fromModels(cls, modelObjects: list[BaseModel]) -> list[BaseSchema]:
        return [CompanyMapper.fromModel(modelObject) for modelObject in modelObjects]
