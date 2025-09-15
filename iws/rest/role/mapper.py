#
# Author: Rohtash Lakra
#
import logging

from framework.orm.mapper import Mapper
from framework.orm.pydantic.model import BaseModel
from framework.orm.sqlalchemy.schema import BaseSchema
from rest.role.model import Role, Permission, Capability
from rest.role.schema import RoleSchema, PermissionSchema, CapabilitySchema

logger = logging.getLogger(__name__)


class RoleMapper(Mapper):

    @classmethod
    def fromSchema(cls, roleSchema: RoleSchema) -> Role:
        logger.debug(f"+fromSchema({roleSchema})")
        role = Role(**roleSchema.toJSONObject())
        logger.debug(f"role={role}")
        logger.debug(f"role={role}, roleSchema.permissions={roleSchema.permissions}")
        if roleSchema.permissions:
            role.permissions = [PermissionMapper.fromSchema(permissionSchema) for permissionSchema in
                                roleSchema.permissions] if roleSchema.permissions else None
        logger.debug(f"-fromSchema(), role={role}")
        return role

    @classmethod
    def fromModel(cls, roleModel: Role) -> RoleSchema:
        logger.debug(f"+fromModel({roleModel})")
        roleSchema = RoleSchema(**roleModel.toJSONObject())
        logger.debug(f"roleSchema={roleSchema}, roleModel.permissions={roleModel.permissions}")
        if roleModel.permissions:
            roleSchema.permissions = [PermissionMapper.fromModel(permissionModel) for permissionModel in
                                      roleModel.permissions] if roleModel.permissions else None
        logger.debug(f"-fromModel(), roleSchema={roleSchema}")
        return roleSchema

    @classmethod
    def fromSchemas(cls, schemaObjects: list[BaseSchema]) -> list[BaseModel]:
        return [RoleMapper.fromSchema(schemaObject) for schemaObject in schemaObjects]

    @classmethod
    def fromModels(cls, modelObjects: list[BaseModel]) -> list[BaseSchema]:
        return [RoleMapper.fromModel(modelObject) for modelObject in modelObjects]


class PermissionMapper(Mapper):

    @classmethod
    def fromSchema(cls, permissionSchema: PermissionSchema) -> Permission:
        logger.debug(f"+fromSchema({permissionSchema})")
        permission = Permission(**permissionSchema.toJSONObject())
        logger.debug(f"-fromSchema(), permission={permission}")
        return permission

    @classmethod
    def fromModel(cls, permissionModel: Permission) -> PermissionSchema:
        logger.debug(f"+fromModel({permissionModel})")
        permissionSchema = PermissionSchema(**permissionModel.toJSONObject())
        logger.debug(f"-fromModel(), permissionSchema={permissionSchema}")
        return permissionSchema

    @classmethod
    def fromSchemas(cls, schemaObjects: list[BaseSchema]) -> list[BaseModel]:
        return [PermissionMapper.fromSchema(schemaObject) for schemaObject in schemaObjects]

    @classmethod
    def fromModels(cls, modelObjects: list[BaseModel]) -> list[BaseSchema]:
        return [PermissionMapper.fromModel(modelObject) for modelObject in modelObjects]


class CapabilityMapper(Mapper):

    @classmethod
    def fromSchema(cls, schemaObject: CapabilitySchema) -> Capability:
        logger.debug(f"+fromSchema({schemaObject})")
        modelObject = Capability(**schemaObject.toJSONObject())
        logger.debug(f"-fromSchema(), modelObject={modelObject}")
        return modelObject

    @classmethod
    def fromModel(cls, modelObject: Capability) -> CapabilitySchema:
        logger.debug(f"+fromModel({modelObject})")
        schemaObject = CapabilitySchema(**modelObject.toJSONObject())
        logger.debug(f"-fromModel(), schemaObject={schemaObject}")
        return schemaObject

    @classmethod
    def fromSchemas(cls, schemaObjects: list[BaseSchema]) -> list[BaseModel]:
        return [CapabilityMapper.fromSchema(schemaObject) for schemaObject in schemaObjects]

    @classmethod
    def fromModels(cls, modelObjects: list[BaseModel]) -> list[BaseSchema]:
        return [CapabilityMapper.fromModel(modelObject) for modelObject in modelObjects]
