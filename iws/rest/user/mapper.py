#
# Author: Rohtash Lakra
#
import logging

from framework.orm.mapper import Mapper
from framework.orm.pydantic.model import BaseModel
from framework.orm.sqlalchemy.schema import BaseSchema
from rest.user.model import User, Address, UserSecurity
from rest.user.schema import UserSchema, AddressSchema, UserSecuritySchema

logger = logging.getLogger(__name__)


class UserMapper(Mapper):

    @classmethod
    # @override
    def fromSchema(cls, schemaObject: UserSchema) -> User:
        logger.debug(f"+fromSchema({schemaObject})")
        modelObject = User(**schemaObject.toJSONObject())
        if schemaObject.addresses:
            logger.debug(f"schemaObject={schemaObject}, schemaObject.addresses={schemaObject.addresses}")
            modelObject.addresses = [AddressMapper.fromSchema(address) for address in
                                     schemaObject.addresses] if schemaObject.addresses else None
        # user_security
        # modelObject.user_security = UserSecurityMapper.fromSchema(
        #     schemaObject.user_security) if schemaObject.user_security else None

        logger.debug(f"-fromSchema(), modelObject={modelObject}")
        return modelObject

    @classmethod
    # @override
    def fromModel(cls, modelObject: User) -> UserSchema:
        logger.debug(f"+fromModel({modelObject})")
        schemaObject = UserSchema(**modelObject.toJSONObject())
        if modelObject.addresses:
            logger.debug(f"modelObject={modelObject}, modelObject.addresses={modelObject.addresses}")
            schemaObject.addresses = [AddressMapper.fromModel(address) for address in
                                      modelObject.addresses] if modelObject.addresses else None

        # user_security
        logger.debug(f"modelObject.user_security={modelObject.user_security}")
        schemaObject.user_security = UserSecurityMapper.fromModel(
            modelObject.user_security) if modelObject.user_security else None

        logger.debug(f"-fromModel(), schemaObject={schemaObject}")
        return schemaObject

    @classmethod
    def fromSchemas(cls, schemaObjects: list[BaseSchema]) -> list[BaseModel]:
        return [UserMapper.fromSchema(schemaObject) for schemaObject in schemaObjects]

    @classmethod
    def fromModels(cls, modelObjects: list[BaseModel]) -> list[BaseSchema]:
        return [UserMapper.fromModel(modelObject) for modelObject in modelObjects]


class UserSecurityMapper(Mapper):

    @classmethod
    def fromSchema(cls, schemaObject: UserSecuritySchema) -> UserSecurity:
        # logger.debug(f"+fromSchema(), schemaObject={schemaObject}")
        return UserSecurity(**schemaObject.toJSONObject())

    @classmethod
    def fromModel(cls, modelObject: UserSecurity) -> UserSecuritySchema:
        # logger.debug(f"+fromModel(), modelObject={modelObject}")
        return UserSecuritySchema(**modelObject.toJSONObject())

    @classmethod
    def fromSchemas(cls, schemaObjects: list[BaseSchema]) -> list[BaseModel]:
        return [UserSecurityMapper.fromSchema(schemaObject) for schemaObject in schemaObjects]

    @classmethod
    def fromModels(cls, modelObjects: list[BaseModel]) -> list[BaseSchema]:
        return [UserSecurityMapper.fromModel(modelObject) for modelObject in modelObjects]


class AddressMapper(Mapper):

    @classmethod
    def fromSchema(cls, schemaObject: AddressSchema) -> Address:
        # logger.debug(f"+fromSchema(), schemaObject={schemaObject}")
        return Address(**schemaObject.toJSONObject())

    @classmethod
    def fromModel(cls, modelObject: Address) -> AddressSchema:
        # logger.debug(f"+fromModel(), modelObject={modelObject}")
        return AddressSchema(**modelObject.toJSONObject())

    @classmethod
    def fromSchemas(cls, schemaObjects: list[BaseSchema]) -> list[BaseModel]:
        return [AddressMapper.fromSchema(schemaObject) for schemaObject in schemaObjects]

    @classmethod
    def fromModels(cls, modelObjects: list[BaseModel]) -> list[BaseSchema]:
        return [AddressMapper.fromModel(modelObject) for modelObject in modelObjects]
