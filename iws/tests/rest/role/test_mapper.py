import logging
import unittest

from framework.datetime import nowMillis
from rest.role.mapper import RoleMapper, PermissionMapper, CapabilityMapper
from rest.role.model import Role, Permission, Capability
from rest.role.schema import RoleSchema, PermissionSchema, CapabilitySchema
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class RoleMapperTest(AbstractTestCase):
    """Unit-tests for Mapper classes"""

    def test_role_mappers(self):
        logger.debug("+test_role_mappers()")
        expected = "<class 'rest.role.mapper.RoleMapper'>"
        self.assertEqual(expected, str(RoleMapper))

        expected = "<class 'rest.role.mapper.PermissionMapper'>"
        self.assertEqual(expected, str(PermissionMapper))
        logger.debug("-test_role_mappers()")
        print()

    def assertRoleSchemaAndRole(self, roleSchema: RoleSchema, role: Role):
        """Asserts the schema and model objects."""
        logger.debug(f"assertRoleSchemaAndRole(), roleSchema={roleSchema}, role={role}")
        self.assertEqual(roleSchema.id, role.id)
        self.assertEqual(roleSchema.name, role.name)
        self.assertEqual(roleSchema.active, role.active)
        self.assertEqual(roleSchema.meta_data, role.meta_data)

    def test_role_fromSchema(self):
        logger.debug("+test_role_fromSchema()")
        # create a role
        testRoleSchema = RoleSchema(name=f"TestRole-{nowMillis()}", active=True,
                                    meta_data={"description": "A TestRole"})
        logger.debug(f"testRoleSchema={testRoleSchema}")
        self.assertIsNotNone(testRoleSchema)
        testRole = RoleMapper.fromSchema(testRoleSchema)
        logger.debug(f"testRole={testRole}")
        self.assertIsNotNone(testRole)

        # validate objects
        self.assertRoleSchemaAndRole(testRoleSchema, testRole)
        logger.debug("-test_role_fromSchema()")
        print()

    def test_role_fromModel(self):
        logger.debug("+test_role_fromModel()")
        # create a role
        testRole = Role(name=f"TestRole-{nowMillis()}", active=True, meta_data={"description": "A TestRole"})
        logger.debug(f"testRole={testRole}")
        self.assertIsNotNone(testRole)
        testRoleSchema = RoleMapper.fromModel(testRole)
        logger.debug(f"testRoleSchema={testRoleSchema}")
        self.assertIsNotNone(testRoleSchema)

        # validate objects
        self.assertRoleSchemaAndRole(testRoleSchema, testRole)
        logger.debug("-test_role_fromModel()")
        print()

    def assertPermissionSchemaAndPermission(self, permissionSchema: PermissionSchema, permission: Permission):
        """Asserts the schema and model objects."""
        logger.debug(
            f"assertPermissionSchemaAndPermission(), permissionSchema={permissionSchema}, Permission={Permission}")
        self.assertEqual(permissionSchema.id, permission.id)
        self.assertEqual(permissionSchema.name, permission.name)
        self.assertEqual(permissionSchema.description, permission.description)
        self.assertEqual(permissionSchema.active, permission.active)

    def test_permission_fromSchema(self):
        logger.debug("+test_permission_fromSchema()")
        # create a permission
        permissionName = f"Read-{nowMillis()}"
        permission_json = {
            "name": permissionName,
            "active": True,
            "description": "Read Role"
        }

        permissionSchema = PermissionSchema(**permission_json)
        logger.debug(f"permissionSchema={permissionSchema}")
        self.assertIsNotNone(permissionSchema)
        permission = PermissionMapper.fromSchema(permissionSchema)
        logger.debug(f"permission={permission}")
        self.assertIsNotNone(permission)

        # validate objects
        self.assertPermissionSchemaAndPermission(permissionSchema, permission)
        logger.debug("-test_permission_fromSchema()")
        print()

    def test_permission_fromModel(self):
        logger.debug("+test_permission_fromModel()")
        # create a permission
        permissionName = f"Read-{nowMillis()}"
        permission_json = {
            "name": permissionName,
            "active": True,
            "description": "Read Role"
        }

        permission = Permission(**permission_json)
        logger.debug(f"permission={permission}")
        self.assertIsNotNone(permission)
        permissionSchema = PermissionMapper.fromModel(permission)
        logger.debug(f"permissionSchema={permissionSchema}")
        self.assertIsNotNone(permissionSchema)

        # validate objects
        self.assertPermissionSchemaAndPermission(permissionSchema, permission)
        logger.debug("-test_permission_fromModel()")
        print()

    def test_role_fromModel_with_permission(self):
        logger.debug("+test_role_fromModel_with_permission()")
        # Create roles
        readOnlyRole = Role(name=f"ReadOnly-{nowMillis()}", active=True, meta_data={"description": "A ReadOnly Role"})
        logger.debug(f"readOnlyRole={readOnlyRole}")
        self.assertIsNotNone(readOnlyRole)

        # Create permissions
        readPermission = Permission(name=f"Read-{nowMillis()}", description="Allows read access", active=True)
        logger.debug(f"readPermission={readPermission}")

        # Assign permissions to roles
        readOnlyRole.permissions = []
        readOnlyRole.permissions.append(readPermission)
        logger.debug(f"readOnlyRole={readOnlyRole}")
        self.assertIsNotNone(readOnlyRole.permissions)

        readOnlyRoleSchema = RoleMapper.fromModel(readOnlyRole)
        logger.debug(f"readOnlyRoleSchema={readOnlyRoleSchema}")
        self.assertIsNotNone(readOnlyRoleSchema)

        self.assertRoleSchemaAndRole(readOnlyRoleSchema, readOnlyRole)
        self.assertIsNotNone(readOnlyRole.permissions)
        self.assertIsNotNone(readOnlyRoleSchema.permissions)
        self.assertEqual(1, len(readOnlyRole.permissions))
        self.assertEqual(1, len(readOnlyRoleSchema.permissions))

        # asset role's permission
        self.assertPermissionSchemaAndPermission(readOnlyRoleSchema.permissions[0], readPermission)
        logger.debug("-test_role_fromModel_with_permission()")
        print()

    def assertCapabilitySchemaAndCapability(self, expectedObject: CapabilitySchema, actualObject: Capability):
        """Asserts the schema and model objects."""
        logger.debug(
            f"assertCapabilitySchemaAndCapability(), expectedObject={expectedObject}, actualObject={actualObject}")
        self.assertEqual(expectedObject.id, actualObject.id)
        self.assertEqual(expectedObject.name, actualObject.name)
        self.assertEqual(expectedObject.description, actualObject.description)
        self.assertEqual(expectedObject.active, actualObject.active)

    def test_capability_fromSchema(self):
        logger.debug("+test_capability_fromSchema()")
        # create a capability
        capabilityName = f"Create-{nowMillis()}"
        capability_json = {
            "name": capabilityName,
            "active": True,
            "description": "Create Capability"
        }

        capabilitySchema = CapabilitySchema(**capability_json)
        logger.debug(f"capabilitySchema={capabilitySchema}")
        self.assertIsNotNone(capabilitySchema)
        capability = CapabilityMapper.fromSchema(capabilitySchema)
        logger.debug(f"capability={capability}")
        self.assertIsNotNone(capability)

        # validate objects
        self.assertCapabilitySchemaAndCapability(capabilitySchema, capability)
        logger.debug("-test_capability_fromSchema()")
        print()

    def test_capability_fromModel(self):
        logger.debug("+test_capability_fromModel()")
        # create a capability
        capabilityName = f"Create-{nowMillis()}"
        capability_json = {
            "name": capabilityName,
            "active": True,
            "description": "Create Capability"
        }

        capability = Capability(**capability_json)
        logger.debug(f"capability={capability}")
        self.assertIsNotNone(capability)
        capabilitySchema = CapabilityMapper.fromModel(capability)
        logger.debug(f"capabilitySchema={capabilitySchema}")
        self.assertIsNotNone(capabilitySchema)

        # validate objects
        self.assertCapabilitySchemaAndCapability(capabilitySchema, capability)
        logger.debug("-test_capability_fromModel()")
        print()


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
