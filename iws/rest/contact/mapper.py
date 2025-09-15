#
# Author: Rohtash Lakra
#
from framework.orm.mapper import Mapper
from framework.orm.pydantic.model import BaseModel
from framework.orm.sqlalchemy.schema import BaseSchema
from rest.contact.model import Contact
from rest.contact.schema import ContactSchema


class ContactMapper(Mapper):

    @classmethod
    def fromSchema(cls, schemaObject: ContactSchema) -> Contact:
        # logger.debug(f"+fromSchema(), schemaObject={schemaObject}")
        return Contact(**schemaObject.toJSONObject())

    @classmethod
    def fromModel(cls, modelObject: Contact) -> ContactSchema:
        # logger.debug(f"+fromModel(), modelObject={modelObject}")
        return ContactSchema(**modelObject.toJSONObject())

    @classmethod
    def fromSchemas(cls, schemaObjects: list[BaseSchema]) -> list[BaseModel]:
        return [ContactMapper.fromSchema(schemaObject) for schemaObject in schemaObjects]

    @classmethod
    def fromModels(cls, modelObjects: list[BaseModel]) -> list[BaseSchema]:
        return [ContactMapper.fromModel(modelObject) for modelObject in modelObjects]
