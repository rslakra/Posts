import logging
import unittest

from framework.exception import ValidationException
from framework.http import HTTPStatus
from framework.orm.sqlalchemy.schema import SchemaOperation
from framework.time import timeMillis
from rest.role.model import Role, Permission
from rest.role.service import RoleService
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class RoleServiceTest(AbstractTestCase):
    """Unit-tests for Service class"""

    def setUp(self):
        """The setUp() method of the TestCase class is automatically invoked before each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+setUp()")
        super().setUp()

        # toString() test
        expected = "<class 'rest.role.service.RoleService'>"
        self.assertEqual(expected, str(RoleService))

        # init object
        self.role = Role(name=f"ServiceRole-{timeMillis()}", active=True, meta_data={"description": "A service role"})
        self.readPermission = Permission(name=f"Read-{timeMillis()}", description="Allows read access", active=True)
        self.roleService = RoleService()
        logger.debug(f"roleService={self.roleService}")
        self.assertIsNotNone(self.roleService)
        logger.debug("-setUp()")
        print()

    def tearDown(self):
        """The tearDown() method of the TestCase class is automatically invoked after each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+tearDown()")
        self.role = None
        self.readPermission = None
        self.roleService = None
        self.assertIsNone(self.role)
        self.assertIsNone(self.readPermission)
        self.assertIsNone(self.roleService)
        super().tearDown()
        logger.debug("-tearDown()")
        print()

    def test_validate_error(self):
        logger.debug("+test_validate_error()")
        invalidRole = None
        with self.assertRaises(ValidationException) as context:
            self.roleService.validate(SchemaOperation.CREATE, invalidRole)

        # validate exception
        logger.debug(f"context={context}, context.exception={context.exception}")
        self.assertTrue(type(context.exception) in [ValidationException])
        validationException = context.exception
        self.assertEqual(HTTPStatus.INVALID_DATA, validationException.httpStatus)
        self.assertLess(0, len(validationException.messages))
        self.assertEqual("'Role' is not fully defined!", validationException.messages[0])

        # update validation
        with self.assertRaises(ValidationException) as context:
            self.roleService.validate(SchemaOperation.UPDATE, invalidRole)

        # validate exception
        logger.debug(f"context={context}, context.exception={context.exception}")
        self.assertTrue(type(context.exception) in [ValidationException])
        validationException = context.exception
        self.assertEqual(HTTPStatus.INVALID_DATA, validationException.httpStatus)
        self.assertLess(0, len(validationException.messages))
        self.assertEqual("'Role' is not fully defined!", validationException.messages[0])

        logger.debug("-test_validate_error()")
        print()

    def test_validate_success(self):
        logger.debug("+test_validate()")
        self.roleService.validate(SchemaOperation.CREATE, self.role)
        logger.debug("-test_validate()")
        print()

    def test_findByFilter(self):
        logger.debug("+test_findByFilter()")
        roleModels = self.roleService.findByFilter(None)
        logger.debug(f"roleModels={roleModels}")
        self.assertIsNotNone(roleModels)
        self.assertLess(0, len(roleModels))
        logger.debug("-test_findByFilter()")
        print()

    def test_existsByFilter(self):
        logger.debug("+test_existsByFilter()")
        result = self.roleService.existsByFilter({"name": "ReadOnly"})
        logger.debug(f"result={result}")
        self.assertIsNotNone(result)
        self.assertEqual(False, result)
        logger.debug("-test_existsByFilter()")
        print()

    def test_create_role(self):
        logger.debug("+test_create_role()")
        logger.debug(f"role={self.role}")
        self.role = self.roleService.create(self.role)
        logger.debug(f"role={self.role}")
        self.assertIsNotNone(self.role)
        self.assertIsNotNone(self.role.id)
        self.assertTrue(self.role.name.startswith("ServiceRole"))
        logger.debug("-test_create_role()")
        print()

    def test_create_role_with_permissions(self):
        logger.debug("+test_create_role_with_permissions()")
        roleName = f"MultiPermissions-{timeMillis()}"
        roleWithPermissions = Role(name=roleName)
        readPermission = Permission(name=f"Read-{timeMillis()}", description="Allows read access", active=True)
        writePermission = Permission(name=f"Write-{timeMillis()}", description="Allows write access", active=True)
        executePermission = Permission(name=f"Execute-{timeMillis()}", description="Allows execute access", active=True)
        roleWithPermissions.permissions.extend([readPermission, writePermission, executePermission])
        logger.debug(f"roleWithPermissions={roleWithPermissions}")

        # create a role with permissions
        roleWithPermissions = self.roleService.create(roleWithPermissions)
        logger.debug(f"roleWithPermissions={roleWithPermissions}")
        self.assertIsNotNone(roleWithPermissions)
        self.assertIsNotNone(roleWithPermissions.id)
        self.assertEqual(roleName, roleWithPermissions.name)
        self.assertEqual(3, len(roleWithPermissions.permissions))

        for permission in roleWithPermissions.permissions:
            self.assertIsNotNone(permission.id)

        logger.debug("-test_create_role_with_permissions()")
        print()

    def test_update_role(self):
        logger.debug("+test_update_role()")
        # update it
        logger.debug(f"role={self.role}")
        self.role = self.roleService.create(self.role)
        logger.debug(f"role={self.role}")
        updatedMetadata = {"description": "An updated service role"}
        self.role.meta_data = updatedMetadata
        self.role = self.roleService.update(self.role)
        logger.debug(f"role={self.role}")
        self.assertIsNotNone(self.role)
        self.assertIsNotNone(self.role.id)
        self.assertEqual(updatedMetadata, self.role.meta_data)
        logger.debug("-test_update_role()")
        print()

    def test_delete_role(self):
        logger.debug("+test_delete_role()")
        # delete it
        logger.debug(f"role={self.role}")
        self.role = self.roleService.create(self.role)
        logger.debug(f"role={self.role}")
        self.assertIsNotNone(self.role)
        self.assertIsNotNone(self.role.id)
        self.roleService.delete(self.role.id)
        logger.debug("-test_delete_role()")
        print()


# Starting point
if __name__ == 'main':
    super()
    unittest.main(exit=False)
