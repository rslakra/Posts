import logging
import unittest

from framework.time import timeMillis
from rest.role.repository import RoleRepository, PermissionRepository
from rest.role.schema import RoleSchema, PermissionSchema
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class RoleRepositoryTest(AbstractTestCase):
    """Unit-tests for Repository classes"""

    def setUp(self):
        """The setUp() method of the TestCase class is automatically invoked before each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+setUp()")
        super().setUp()

        # toString() test
        expected = "<class 'rest.role.repository.RoleRepository'>"
        self.assertEqual(expected, str(RoleRepository))

        # init object
        self.roleRepository = RoleRepository()
        logger.debug(f"roleRepository={self.roleRepository}")
        self.assertIsNotNone(self.roleRepository)
        expected = 'RoleRepository <engine=Engine(sqlite:///testPosts.db)>'
        self.assertEqual(expected, str(self.roleRepository))
        self.assertIsNotNone(self.roleRepository.get_engine())

        self.permissionRepository = PermissionRepository()
        logger.debug(f"permissionRepository={self.permissionRepository}")
        self.assertIsNotNone(self.permissionRepository)
        expected = 'PermissionRepository <engine=Engine(sqlite:///testPosts.db)>'
        self.assertEqual(expected, str(self.permissionRepository))
        self.assertIsNotNone(self.permissionRepository.get_engine())
        logger.debug("-setUp()")
        print()

    def tearDown(self):
        """The tearDown() method of the TestCase class is automatically invoked after each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+tearDown()")
        self.permissionRepository = None
        self.assertIsNone(self.permissionRepository)
        self.roleRepository = None
        self.assertIsNone(self.roleRepository)
        super().tearDown()
        logger.debug("-tearDown()")
        print()

    def test_create_role(self):
        logger.debug("+test_create_role()")
        # create a role
        roleName = f"Test-{timeMillis()}"
        role_json = {
            "name": roleName,
            "active": True,
            "meta_data": {
                "description": "Role's Metadata Description"
            }
        }

        roleSchema = RoleSchema(**role_json)
        logger.debug(f"roleSchema={roleSchema}")
        roleSchema = self.roleRepository.save(roleSchema)
        logger.debug(f"roleSchema={roleSchema}")
        self.assertIsNotNone(roleSchema.id)
        self.assertEqual(roleName, roleSchema.name)
        self.assertEqual(True, roleSchema.active)
        logger.debug("-test_create_role()")
        print()

    def test_create_permission(self):
        logger.debug("+test_create_permission()")
        # Basic CRUD operations:
        # "Create", "Read", "Update", "Delete" are often the fundamental permissions for managing data within a system.

        permissionName = f"Read-{timeMillis()}"
        permission_json = {
            "name": permissionName,
            "description": "Allows read access",
            "active": True,
        }

        permissionSchema = PermissionSchema(**permission_json)
        logger.debug(f"permissionSchema={permissionSchema}")
        permissionSchema = self.permissionRepository.save(permissionSchema)
        logger.debug(f"permissionSchema={permissionSchema}")
        self.assertIsNotNone(permissionSchema.id)
        self.assertEqual(permissionName, permissionSchema.name)
        self.assertEqual(True, permissionSchema.active)
        logger.debug("-test_create_permission()")
        print()

    def assertPermissionSchema(self, expected: PermissionSchema, actual: PermissionSchema):
        """Asserts the contact's schema objects."""
        logger.debug(f"expected={expected}")
        logger.debug(f"actual={actual}")
        self.assertEqual(expected.id, actual.id)
        self.assertEqual(expected.name, actual.name)
        self.assertEqual(expected.active, actual.active)
        self.assertEqual(str(expected), str(actual))

    def test_create_role_with_permission(self):
        logger.debug("+test_create_role_with_permission()")
        # Create roles
        adminRole = RoleSchema(name=f"Admin-{timeMillis()}", active=True, meta_data={"description": "An Admin Role"})
        editorRole = RoleSchema(name=f"Editor-{timeMillis()}", active=True, meta_data={"description": "An Editor Role"})
        logger.debug(f"adminRole={adminRole}")
        logger.debug(f"editorRole={editorRole}")

        # Create permissions
        readPermission = PermissionSchema(name=f"Read-{timeMillis()}", description="Allows read access", active=True)
        writePermission = PermissionSchema(name=f"Write-{timeMillis()}", description="Allows write access", active=True)
        logger.debug(f"readPermission={readPermission}")
        logger.debug(f"writePermission={writePermission}")

        # Assign permissions to roles
        adminRole.permissions.append(readPermission)
        adminRole.permissions.append(writePermission)
        editorRole.permissions.append(readPermission)
        logger.debug(f"adminRole={adminRole}")
        logger.debug(f"editorRole={editorRole}")

        # persist roles and permissions
        self.roleRepository.save_all([adminRole, editorRole, readPermission, writePermission])

        # find roles and validate
        # self.roleRepository.save_all([adminRole, editorRole])
        adminRole = self.roleRepository.filter({"name": adminRole.name})[0]
        logger.debug(f"adminRole={adminRole}")
        self.assertIsNotNone(adminRole.id)
        self.assertIsNotNone(adminRole.permissions)
        self.assertEqual(2, len(adminRole.permissions))

        editorRole = self.roleRepository.filter({"name": editorRole.name})[0]
        logger.debug(f"editorRole={editorRole}")
        self.assertIsNotNone(editorRole.id)
        self.assertIsNotNone(editorRole.permissions)
        self.assertEqual(1, len(editorRole.permissions))

        # find permissions and validate
        # self.permissionRepository.save_all([readPermission, writePermission])
        readPermission = self.permissionRepository.filter({"name": readPermission.name})[0]
        logger.debug(f"readPermission={readPermission}")
        self.assertIsNotNone(readPermission.id)
        writePermission = self.permissionRepository.filter({"name": writePermission.name})[0]
        logger.debug(f"writePermission={writePermission}")
        self.assertIsNotNone(writePermission.id)

        # asset role's permission
        self.assertPermissionSchema(adminRole.permissions[0], readPermission)
        self.assertPermissionSchema(adminRole.permissions[1], writePermission)
        self.assertPermissionSchema(editorRole.permissions[0], readPermission)
        logger.debug("-test_create_role_with_permission()")
        print()

        # # Create a user and assign them roles
        # user = User(username="john")
        # user.roles.append(admin_role)
        # session.add(user)
        #
        # # Assign permissions to roles
        # admin_role.permissions.append(read_permission)
        # admin_role.permissions.append(write_permission)
        # editor_role.permissions.append(read_permission)
        # session.commit()
        #
        # # Check if a user has a specific permission
        # def has_permission(user, permission_name):
        #     for role in user.roles:
        #         for permission in role.permissions:
        #             if permission.name == permission_name:
        #                 return True
        #     return False
        #
        # print(has_permission(user, "write"))  # True

    def test_assign_permission(self):
        logger.debug("+test_assign_permission()")
        # Create roles
        adminRole = RoleSchema(name=f"Admin-{timeMillis()}", active=True, meta_data={"description": "An Admin Role"})
        logger.debug(f"adminRole={adminRole}")

        # Create permissions
        readPermission = PermissionSchema(name=f"Read-{timeMillis()}", description="Allows read access", active=True)
        writePermission = PermissionSchema(name=f"Write-{timeMillis()}", description="Allows write access", active=True)
        logger.debug(f"readPermission={readPermission}")
        logger.debug(f"writePermission={writePermission}")

        # persist roles and permissions
        self.roleRepository.save_all([adminRole, readPermission, writePermission])
        # validate role
        adminRole = self.roleRepository.filter({"name": adminRole.name})[0]
        logger.debug(f"adminRole={adminRole}")
        self.assertIsNotNone(adminRole.id)
        self.assertIsNotNone(adminRole.permissions)

        # validate permissions
        readPermission = self.permissionRepository.filter({"name": readPermission.name})[0]
        logger.debug(f"readPermission={readPermission}")
        self.assertIsNotNone(readPermission.id)

        writePermission = self.permissionRepository.filter({"name": writePermission.name})[0]
        logger.debug(f"writePermission={writePermission}")
        self.assertIsNotNone(writePermission.id)

        # Assign permissions to roles
        adminRole.permissions.append(readPermission)
        adminRole.permissions.append(writePermission)
        logger.debug(f"adminRole={adminRole}")

        # persist roles and permissions
        adminRole = self.roleRepository.save(adminRole)

        # find roles and validate
        # self.roleRepository.save_all([adminRole, editorRole])
        adminRole = self.roleRepository.filter({"name": adminRole.name})[0]
        logger.debug(f"adminRole={adminRole}")
        self.assertIsNotNone(adminRole.id)
        self.assertIsNotNone(adminRole.permissions)
        self.assertEqual(2, len(adminRole.permissions))

        # asset role's permission
        self.assertPermissionSchema(adminRole.permissions[0], readPermission)
        self.assertPermissionSchema(adminRole.permissions[1], writePermission)
        logger.debug("-test_assign_permission()")
        print()


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
