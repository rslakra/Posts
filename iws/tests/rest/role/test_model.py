import logging
import unittest

from pydantic import ValidationError

from framework.time import timeMillis
from rest.role.model import Role, Permission
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class RoleModelTest(AbstractTestCase):
    """Unit-tests for Service class"""

    def test_preValidator(self):
        logger.debug("+test_preValidator()")

        # validate error
        with self.assertRaises(ValidationError) as context:
            invalidRole = Role()

        logger.debug(f"context={context}, context.exception={context.exception}")
        valueError = context.exception
        self.assertTrue(isinstance(context.exception, ValueError))
        str(context.exception).__contains__("'Model' is not fully defined!")

        with self.assertRaises(ValueError) as context:
            role = Role(meta_data={"description": "Role without name"})

        logger.debug(f"context={context}, context.exception={context.exception}")
        valueError = context.exception
        self.assertTrue(isinstance(context.exception, ValueError))
        str(context.exception).__contains__("Role 'name' is required!")

        with self.assertRaises(ValueError) as context:
            role = Role(name=" ", meta_data={"description": "Role without name"})

        logger.debug(f"context={context}, context.exception={context.exception}")
        valueError = context.exception
        self.assertTrue(isinstance(context.exception, ValueError))
        str(context.exception).__contains__("The model 'name' should not be null or empty!")

        logger.debug("-test_validate_error()")
        print()

    def test_create_role(self):
        logger.debug("+test_create_role()")
        # create object
        roleName = f"RoleModel-{timeMillis()}"
        roleModel = Role(name=roleName, active=True, meta_data={"description": "A model's role"})
        logger.debug(f"roleModel={roleModel}")
        self.assertIsNotNone(roleModel)
        self.assertEqual(roleName, roleModel.name)
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

        self.assertIsNotNone(roleWithPermissions)
        self.assertEqual(roleName, roleWithPermissions.name)
        self.assertEqual(3, len(roleWithPermissions.permissions))

        logger.debug("-test_create_role_with_permissions()")
        print()


# Starting point
if __name__ == 'main':
    super()
    unittest.main(exit=False)
