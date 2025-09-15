#
# Author: Rohtash Lakra
#
import logging
from typing import List, Optional, Dict, Any

from werkzeug.datastructures import MultiDict

from framework.exception import DuplicateRecordException, ValidationException, RecordNotFoundException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import BaseModel
from framework.orm.sqlalchemy.schema import SchemaOperation
from framework.service import AbstractService
from rest.role.mapper import RoleMapper, PermissionMapper
from rest.role.model import Role, Permission, RoleAssignPermission
from rest.role.repository import RoleRepository, PermissionRepository
from rest.role.schema import PermissionSchema, RoleSchema

logger = logging.getLogger(__name__)


class RoleService(AbstractService):
    """Role's Service"""

    def __init__(self):
        logger.debug("RoleService()")
        self.roleRepository = RoleRepository()
        self.permissionRepository = PermissionRepository()

    def validate(self, operation: SchemaOperation, role: Role) -> None:
        logger.debug(f"+validate({operation}, {role})")
        # super().validate(operation, role)
        error_messages = []

        # validate the object
        if role:
            match operation.name:
                case SchemaOperation.CREATE.name:
                    # validate the required fields
                    if not role.name:
                        error_messages.append("Role 'name' is required!")

                case SchemaOperation.UPDATE.name:
                    if not role.id:
                        error_messages.append("Role 'id' is required!")
        else:
            error_messages.append("'Role' is not fully defined!")

        # throw an error if any validation error
        logger.debug(f"{type(error_messages)} => error_messages={error_messages}")
        if error_messages and len(error_messages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=error_messages)
            logger.debug(f"{type(error)} = exception={error}")
            raise error

        logger.debug(f"-validate()")

    # @override
    def findByFilter(self, filters: Dict[str, Any]) -> List[Optional[BaseModel]]:
        logger.debug(f"+findByFilter({filters})")
        roleSchemas = self.roleRepository.filter(filters)
        # logger.debug(f"roleSchemas => type={type(roleSchemas)}, values={roleSchemas}")
        roleModels = []
        for roleSchema in roleSchemas:
            # logger.debug(f"roleSchema type={type(roleSchema)}, value={roleSchema}")
            roleModel = RoleMapper.fromSchema(roleSchema)
            # logger.debug(f"type={type(roleModel)}, roleModel={roleModel}")
            roleModels.append(roleModel)
            # roleModelValidate = Role.model_validate(roleSchema)
            # logger.debug(f"type={type(roleModelValidate)}, roleModelValidate={roleModelValidate}")

        logger.debug(f"-findByFilter(), roleModels={roleModels}")
        return roleModels

    # @override
    def existsByFilter(self, filters: Dict[str, Any]) -> bool:
        """Returns True if the records exist by filter otherwise False"""
        logger.debug(f"+existsByFilter({filters})")
        roleSchemas = self.roleRepository.filter(filters)
        result = True if roleSchemas else False
        logger.debug(f"-existsByFilter(), result={result}")
        return result

    def validates(self, operation: SchemaOperation, roles: List[Role]) -> None:
        logger.debug(f"+validates({operation}, {roles})")
        error_messages = []

        # validate the object
        if not roles:
            error_messages.append('Roles is required!')

        for role in roles:
            self.validate(operation, role)

        # throw an error if any validation error
        if error_messages and len(error_messages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=error_messages)
            logger.debug(f"{type(error)} = exception={error}")
            raise error

        logger.debug(f"-validates()")

    def create(self, role: Role) -> Role:
        """Crates a new role"""
        logger.debug(f"+create({role})")
        if self.existsByFilter({"name": role.name}):
            raise DuplicateRecordException(HTTPStatus.CONFLICT, f"[{role.name}] role already exists!")

        # role = self.repository.create(role)
        roleSchema = RoleMapper.fromModel(role)
        roleSchema = self.roleRepository.save(roleSchema)
        if roleSchema and roleSchema.id is None:
            roleSchema = self.roleRepository.filter({"name": role.name})

        role = RoleMapper.fromSchema(roleSchema)
        # role = Role.model_validate(roleSchema)

        logger.debug(f"-create(), role={role}")
        return role

    def bulkCreate(self, roles: List[Role]) -> List[Role]:
        """Crates a new role"""
        logger.debug(f"+bulkCreate({roles})")
        results = []
        for role in roles:
            result = self.create(role)
            results.append(result)

        logger.debug(f"-bulkCreate(), results={results}")
        return results

    def update(self, role: Role) -> Role:
        """Updates the role"""
        logger.debug(f"+update({role})")
        # self.validate(SchemaOperation.UPDATE, role)
        # check record exists by id
        if not self.existsByFilter({"id": role.id}):
            raise RecordNotFoundException(HTTPStatus.NOT_FOUND, f"Role doesn't exist!")

        roleSchemas = self.roleRepository.filter({"id": role.id})
        roleSchema = roleSchemas[0]
        if role.name and roleSchema.name != role.name:
            roleSchema.name = role.name

        if role.active and roleSchema.active != role.active:
            roleSchema.active = role.active

        if role.meta_data and roleSchema.meta_data != role.meta_data:
            roleSchema.meta_data = role.meta_data

        # roleSchema = CompanyMapper.fromModel(oldRole)
        self.roleRepository.update(roleSchema)
        # roleSchema = self.repository.update(mapper=RoleSchema, mappings=[roleSchema])
        roleSchema = self.roleRepository.filter({"id": role.id})[0]
        role = RoleMapper.fromSchema(roleSchema)
        logger.debug(f"-update(), role={role}")
        return role

    def delete(self, id: int) -> None:
        logger.debug(f"+delete({id})")
        # check record exists by id
        filter = {"id": id}
        if self.existsByFilter(filter):
            self.roleRepository.delete(filter)
        else:
            raise RecordNotFoundException(HTTPStatus.NOT_FOUND, "Role doesn't exist!")

        logger.debug(f"-delete()")

    def assignPermissions(self, rolePermissions: list[RoleAssignPermission]) -> List[Role]:
        """Grants the permissions to the roles"""
        logger.debug(f"+assignPermissions({rolePermissions})")
        schemaObjects = []
        for rolePermission in rolePermissions:
            # load roles
            schemaObject = self.roleRepository.findById(RoleSchema, rolePermission.role_id)
            # load roles permissions
            filterPermissions = MultiDict()
            for id in rolePermission.permissions:
                filterPermissions.add("id", id)

            permissions = self.permissionRepository.filter(filterPermissions)
            if schemaObject and permissions:
                # assign permissions to role
                schemaObject.permissions.extend(permissions)
                schemaObjects.append(schemaObject)

        logger.debug(f"schemaObjects=>{schemaObjects}")
        if schemaObjects:
            self.roleRepository.save_all(schemaObjects)
            filterRoles = MultiDict()
            for schemaObject in schemaObjects:
                filterRoles.add("id", schemaObject.id)
            schemaObjects = self.roleRepository.filter(filterRoles)
            modelObjects = RoleMapper.fromSchemas(schemaObjects)
        else:
            modelObjects = None

        logger.debug(f"-assignPermissions(), modelObjects={modelObjects}")
        return modelObjects

    def revokePermissions(self, rolePermissions: list[RoleAssignPermission]) -> List[Role]:
        """Revokes the permissions of the roles"""
        logger.debug(f"+revokePermissions({rolePermissions})")
        schemaObjects = []
        for rolePermission in rolePermissions:
            # load roles
            schemaObject = self.roleRepository.findById(RoleSchema, rolePermission.role_id)
            revoked = False
            if schemaObject and schemaObject.permissions:
                # schemaObjectPermissions = schemaObject.permissions.copy()
                for schemaObjectPermission in schemaObject.permissions:
                    if schemaObjectPermission.id in rolePermission.permissions:
                        logger.debug(f"Removing schemaObjectPermission={schemaObjectPermission}")
                        schemaObject.permissions.remove(schemaObjectPermission)
                        revoked = True

                # persist role and remove permissions
                if revoked:
                    schemaObject = self.roleRepository.save(schemaObject)
                    schemaObjects.append(schemaObject)

        if schemaObjects:
            modelObjects = RoleMapper.fromSchemas(schemaObjects)
        else:
            modelObjects = None

        logger.debug(f"-revokePermissions(), modelObjects={modelObjects}")
        return modelObjects


class PermissionService(AbstractService):
    """Permission's Service"""

    def __init__(self):
        logger.debug("PermissionService()")
        self.permissionRepository = PermissionRepository()

    def validate(self, operation: SchemaOperation, modelObject: Permission) -> None:
        logger.debug(f"+validate({operation}, {modelObject})")
        # super().validate(operation, role)
        error_messages = []

        # validate the object
        if modelObject:
            match operation.name:
                case SchemaOperation.CREATE.name:
                    # validate the required fields
                    if not modelObject.name:
                        error_messages.append("Permission 'name' is required!")

                case SchemaOperation.UPDATE.name:
                    if not modelObject.id:
                        error_messages.append("Permission 'id' is required!")
        else:
            error_messages.append("'Permission' is not fully defined!")

        # throw an error if any validation error
        logger.debug(f"{type(error_messages)} => error_messages={error_messages}")
        if error_messages and len(error_messages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=error_messages)
            logger.debug(f"{type(error)} = exception={error}")
            raise error

        logger.debug(f"-validate()")

    # @override
    def findByFilter(self, filters: Dict[str, Any]) -> List[Optional[BaseModel]]:
        logger.debug(f"+findByFilter({filters})")
        schemaObjects = self.permissionRepository.filter(filters)
        # logger.debug(f"schemaObjects => type={type(schemaObjects)}, values={schemaObjects}")
        modelObjects = []
        for schemaObject in schemaObjects:
            # logger.debug(f"roleSchema type={type(roleSchema)}, value={roleSchema}")
            modelObject = PermissionMapper.fromSchema(schemaObject)
            # logger.debug(f"type={type(modelObject)}, modelObject={modelObject}")
            modelObjects.append(modelObject)
            # roleModelValidate = Role.model_validate(roleSchema)
            # logger.debug(f"type={type(roleModelValidate)}, roleModelValidate={roleModelValidate}")

        logger.debug(f"-findByFilter(), modelObjects={modelObjects}")
        return modelObjects

    # @override
    def existsByFilter(self, filters: Dict[str, Any]) -> bool:
        """Returns True if the records exist by filter otherwise False"""
        logger.debug(f"+existsByFilter({filters})")
        schemaObjects = self.permissionRepository.filter(filters)
        result = True if schemaObjects else False
        logger.debug(f"-existsByFilter(), result={result}")
        return result

    def validates(self, operation: SchemaOperation, modelObjects: List[Permission]) -> None:
        logger.debug(f"+validates({operation}, {modelObjects})")
        error_messages = []

        # validate the object
        if not modelObjects:
            error_messages.append('Roles is required!')

        for modelObject in modelObjects:
            self.validate(operation, modelObject)

        # throw an error if any validation error
        if error_messages and len(error_messages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=error_messages)
            logger.debug(f"{type(error)} = exception={error}")
            raise error

        logger.debug(f"-validates()")

    def create(self, modelObject: Permission) -> Permission:
        """Crates a new role"""
        logger.debug(f"+create({modelObject})")
        self.validate(SchemaOperation.CREATE, modelObject)
        if self.existsByFilter({"name": modelObject.name}):
            raise DuplicateRecordException(HTTPStatus.CONFLICT, f"[{modelObject.name}] permission already exists!")

        schemaObject = PermissionMapper.fromModel(modelObject)
        schemaObject = self.permissionRepository.save(schemaObject)
        if schemaObject and schemaObject.id is None:
            schemaObject = self.permissionRepository.filter({"name": schemaObject.name})

        modelObject = PermissionMapper.fromSchema(schemaObject)

        logger.debug(f"-create(), modelObject={modelObject}")
        return modelObject

    def bulkCreate(self, modelObjects: List[Permission]) -> List[Permission]:
        """Crates a new role"""
        logger.debug(f"+bulkCreate({modelObjects})")
        results = []
        for modelObject in modelObjects:
            result = self.create(modelObject)
            results.append(result)

        logger.debug(f"-bulkCreate(), results={results}")
        return results

    def update(self, modelObject: Permission) -> Permission:
        """Updates the role"""
        logger.debug(f"+update({modelObject})")
        self.validate(SchemaOperation.UPDATE, modelObject)
        # check record exists by id
        if not self.existsByFilter({"id": modelObject.id}):
            raise RecordNotFoundException(HTTPStatus.NOT_FOUND, f"Permission doesn't exist!")

        schemaObject = self.permissionRepository.findById(PermissionSchema, modelObject.id)
        logger.debug(f"schemaObject={schemaObject}")
        if modelObject.name and schemaObject.name != modelObject.name:
            schemaObject.name = modelObject.name

        if modelObject.description and schemaObject.description != modelObject.description:
            schemaObject.description = modelObject.description

        if modelObject.active and schemaObject.active != modelObject.active:
            schemaObject.active = modelObject.active

        # roleSchema = CompanyMapper.fromModel(oldRole)
        self.permissionRepository.update(schemaObject)
        schemaObject = self.permissionRepository.filter({"id": schemaObject.id})[0]
        modelObject = PermissionMapper.fromSchema(schemaObject)
        logger.debug(f"-update(), modelObject={modelObject}")
        return modelObject

    def delete(self, id: int) -> None:
        logger.debug(f"+delete({id})")
        # check record exists by id
        filter = {"id": id}
        if self.existsByFilter(filter):
            self.permissionRepository.delete(filter)
        else:
            raise RecordNotFoundException(HTTPStatus.NOT_FOUND, "Permission doesn't exist!")

        logger.debug(f"-delete()")
