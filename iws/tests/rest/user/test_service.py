import logging
import unittest

from framework.exception import ValidationException
from framework.http import HTTPStatus
from framework.orm.sqlalchemy.schema import SchemaOperation
from framework.security.jwt import TokenType
from rest.user.model import User, Address, LoginUser
from rest.user.service import UserService
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class UserServiceTest(AbstractTestCase):
    """Unit-tests for Service class"""

    def setUp(self):
        """The setUp() method of the TestCase class is automatically invoked before each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+setUp()")
        super().setUp()

        # toString() test
        expected = "<class 'rest.user.service.UserService'>"
        self.assertEqual(expected, str(UserService))

        # init object
        self.userEmail = super().getTestEmail()
        self.userName = self.userEmail.split("@")[0]
        self.user = User(email=self.userEmail, first_name="Roh", last_name="Lak", birth_date="2024-12-27",
                         user_name=self.userName, password="password")
        logger.debug(f"user={self.user}")
        self.address = Address(street1="123 Test Dr.", city="Hayward", state="California", country="United States",
                               zip="94544")
        logger.debug(f"address={self.address}")
        self.userService = UserService()
        logger.debug(f"userService={self.userService}")
        self.assertIsNotNone(self.userService)
        logger.debug("-setUp()")
        print()

    def tearDown(self):
        """The tearDown() method of the TestCase class is automatically invoked after each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+tearDown()")
        self.userEmail = None
        self.userName = None
        self.user = None
        self.address = None
        self.userService = None
        self.assertIsNone(self.user)
        self.assertIsNone(self.address)
        self.assertIsNone(self.userService)
        super().tearDown()
        logger.debug("-tearDown()")
        print()

    def test_validate_error(self):
        logger.debug("+test_validate_error()")
        invalidUser = None

        logger.debug(f"invalidUser={invalidUser}")
        with self.assertRaises(ValidationException) as context:
            self.userService.validate(SchemaOperation.CREATE, invalidUser)

        # validate exception
        logger.debug(f"context={context}, context.exception={context.exception}")
        self.assertTrue(type(context.exception) in [ValidationException])
        validationException = context.exception
        self.assertEqual(HTTPStatus.INVALID_DATA, validationException.httpStatus)
        self.assertLess(0, len(validationException.messages))
        self.assertEqual("'User' is not fully defined!", validationException.messages[0])

        # userEmail = super().getTestEmail(True)
        # userName = userEmail.split("@")[0]
        invalidUser = User(first_name="Roh", last_name="Lak", birth_date="2024-12-27", password="password")
        logger.debug(f"invalidUser={invalidUser}")
        with self.assertRaises(ValidationException) as context:
            self.userService.validate(SchemaOperation.CREATE, invalidUser)

        # validate exception
        self.assertTrue(type(context.exception) in [ValidationException])
        validationException = context.exception
        self.assertEqual(HTTPStatus.INVALID_DATA, validationException.httpStatus)
        self.assertEquals(2, len(validationException.messages))
        self.assertEqual("User 'email' is required!", validationException.messages[0])
        self.assertEqual("User 'user_name' is required!", validationException.messages[1])

        # update validation
        logger.debug(f"invalidUser={invalidUser}")
        with self.assertRaises(ValidationException) as context:
            self.userService.validate(SchemaOperation.UPDATE, invalidUser)

        # validate exception
        logger.debug(f"context={context}, context.exception={context.exception}")
        self.assertTrue(type(context.exception) in [ValidationException])
        validationException = context.exception
        self.assertEqual(HTTPStatus.INVALID_DATA, validationException.httpStatus)
        self.assertEquals(1, len(validationException.messages))
        self.assertEqual("User 'id' is required!", validationException.messages[0])

        logger.debug("-test_validate_error()")
        print()

    def test_validate_success(self):
        logger.debug("+test_validate()")
        logger.debug(f"user={self.user}")
        self.userService.validate(SchemaOperation.CREATE, self.user)
        logger.debug("-test_validate()")
        print()

    def test_findByFilter(self):
        logger.debug("+test_findByFilter()")
        userModels = self.userService.findByFilter(None)
        self.assertIsNotNone(userModels)
        self.assertLess(1, len(userModels))
        logger.debug("-test_findByFilter()")
        print()

    def test_existsByFilter(self):
        logger.debug("+test_existsByFilter()")
        result = self.userService.existsByFilter({"email": self.userEmail})
        logger.debug(f"result={result}")
        self.assertIsNotNone(result)
        self.assertEqual(False, result)
        logger.debug("-test_existsByFilter()")
        print()

    def test_register_user(self):
        logger.debug("+test_register_user()")
        logger.debug(f"user={self.user}")
        self.user = self.userService.register(self.user)
        logger.debug(f"user={self.user}")
        self.assertIsNotNone(self.user)
        self.assertIsNotNone(self.user.id)
        self.assertEquals("Roh", self.user.first_name)

        # find registered user
        user = self.userService.findByFilter({"email": self.user.email})[0]
        self.assertIsNotNone(user)
        self.assertEqual(self.user.email, user.email)
        logger.debug("-test_register_user()")
        print()

    def test_login_user(self):
        logger.debug("+test_login_user()")
        logger.debug(f"user={self.user}")
        # register
        self.user = self.userService.register(self.user)
        logger.debug(f"user={self.user}")
        self.assertIsNotNone(self.user)
        self.assertIsNotNone(self.user.id)
        self.assertEquals("Roh", self.user.first_name)

        # login
        loginUser = LoginUser(email=self.user.email, password="password")
        # 8QDVOXW4KjfBB2hiq8uNEI+QpvE2bhu71oQ+q9PcP8aoLKhT1g9RP65Mni7QWyJ7VJiSIh3LKAFJPv6fL8aCXqQEsObVrVJ2
        authUser = self.userService.login(loginUser)
        logger.debug(f"authUser={authUser}")
        self.assertIsNotNone(authUser)
        self.assertIsNotNone(authUser.token)
        self.assertEqual(authUser.user_id, self.user.id)

        # authenticate
        userObject = self.userService.authenticate(TokenType.AUTH, authUser.token)
        logger.debug(f"userObject={userObject}")
        self.assertIsNotNone(userObject)
        self.assertEqual(userObject.id, self.user.id)

        logger.debug("-test_login_user()")
        print()

    def test_register_user_with_address(self):
        logger.debug("+test_register_user_with_address()")
        userEmail = super().getTestEmail()
        userName = self.userEmail.split("@")[0]
        user = User(email=userEmail, first_name="Roh", last_name="Lak", birth_date="2024-12-27",
                    user_name=userName, password="password")
        address = Address(street1="123 Test Dr.", city="Hayward", state="California", country="United States",
                          zip="94544")
        logger.debug(f"address={address}")
        user.addresses.append(address)
        logger.debug(f"user={user}")

        # create a user with permissions
        user = self.userService.register(user)
        logger.debug(f"user={user}")
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.id)
        self.assertEqual(userEmail, user.email)
        self.assertEqual(1, len(user.addresses))

        for address in user.addresses:
            self.assertIsNotNone(address.id)

        logger.debug("-test_register_user_with_address()")
        print()

    def test_update_user(self):
        logger.debug("+test_update_user()")
        self.user = self.userService.register(self.user)
        logger.debug(f"user={self.user}")
        self.assertIsNotNone(self.user)
        self.assertIsNotNone(self.user.id)

        # update it
        avatar_url = "avatar-url@avatar.com"
        self.user.avatar_url = avatar_url
        logger.debug(f"user={self.user}")
        self.user = self.userService.update(self.user)
        logger.debug(f"user={self.user}")
        self.assertIsNotNone(self.user)
        self.assertIsNotNone(self.user.id)
        self.assertEqual(avatar_url, self.user.avatar_url)
        logger.debug("-test_update_user()")
        print()

    def test_delete_user(self):
        logger.debug("+test_delete_user()")
        self.user = self.userService.register(self.user)
        logger.debug(f"user={self.user}")
        self.assertIsNotNone(self.user)
        self.assertIsNotNone(self.user.id)

        # delete it
        logger.debug(f"user={self.user}")
        self.userService.delete(self.user.id)
        logger.debug("-test_delete_user()")
        print()


# Starting point
if __name__ == 'main':
    super()
    unittest.main(exit=False)
