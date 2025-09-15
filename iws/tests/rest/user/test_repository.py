import logging
import unittest

from framework.security.hash import HashUtils
from framework.utils import Utils
from rest.user.repository import UserRepository, AddressRepository
from rest.user.schema import UserSchema, UserSecuritySchema, AddressSchema
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class UserRepositoryTest(AbstractTestCase):
    """Unit-tests for Repository classes"""

    def setUp(self):
        """The setUp() method of the TestCase class is automatically invoked before each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+setUp()")
        super().setUp()

        # toString() test
        expected = "<class 'rest.user.repository.UserRepository'>"
        self.assertEqual(expected, str(UserRepository))

        # init object
        self.userRepository = UserRepository()
        logger.debug(f"userRepository={self.userRepository}")
        self.assertIsNotNone(self.userRepository)
        expected = 'UserRepository <engine=Engine(sqlite:///testPosts.db)>'
        self.assertEqual(expected, str(self.userRepository))
        self.assertIsNotNone(self.userRepository.get_engine())

        self.addressRepository = AddressRepository()
        logger.debug(f"addressRepository={self.addressRepository}")
        self.assertIsNotNone(self.addressRepository)
        expected = 'AddressRepository <engine=Engine(sqlite:///testPosts.db)>'
        self.assertEqual(expected, str(self.addressRepository))
        self.assertIsNotNone(self.addressRepository.get_engine())

        logger.debug("-setUp()")
        print()

    def tearDown(self):
        """The tearDown() method of the TestCase class is automatically invoked after each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+tearDown()")
        self.addressRepository = None
        self.assertIsNone(self.addressRepository)
        self.userRepository = None
        self.assertIsNone(self.userRepository)
        super().tearDown()
        logger.debug("-tearDown()")
        print()

    def test_create_user(self):
        logger.debug("+test_create_user()")
        userEmail = super().getTestEmail()
        userName = userEmail.split("@")[0]

        # user
        user_json = {
            "email": userEmail,
            "first_name": "Roh",
            "last_name": "Lak",
            "birth_date": "2024-12-27",
            "user_name": userName,
            "password": "password",
            "admin": False
        }
        userSchema = UserSchema(**user_json)
        logger.debug(f"userSchema={userSchema}")
        userSchema = self.userRepository.save(userSchema)
        logger.debug(f"userSchema={userSchema}")
        self.assertIsNotNone(userSchema.id)
        self.assertEqual(False, userSchema.admin)
        logger.debug("-test_create_user()")
        print()

    def test_create_user_security(self):
        logger.debug("+test_create_user_security()")
        userEmail = super().getTestEmail()
        userName = userEmail.split("@")[0]
        userSchema = UserSchema(email=userEmail, first_name="Roh", last_name="Lak", birth_date="2024-12-27",
                                user_name=userName, password="password")
        logger.debug(f"userSchema={userSchema}")
        userSchema = self.userRepository.save(userSchema)
        logger.debug(f"userSchema={userSchema}")
        self.assertIsNotNone(userSchema.id)
        self.assertEqual(False, userSchema.admin)

        # userSecurity
        salt = Utils.randomUUID()
        passwordHashCode = HashUtils.hashCode(userSchema.password)
        userSecuritySchema = UserSecuritySchema(platform="Python", salt=salt, hashed_auth_token=passwordHashCode)
        logger.debug(f"userSecuritySchema={userSecuritySchema}")
        userSchema.user_security = userSecuritySchema
        # userSecuritySchema.user = userSchema
        userSecuritySchema = self.userRepository.save(userSecuritySchema)
        logger.debug(f"userSecuritySchema={userSecuritySchema}")
        self.assertIsNotNone(userSecuritySchema.user_id)
        self.assertEqual("Python", userSecuritySchema.platform)
        self.assertEqual(salt, userSecuritySchema.salt)
        self.assertEqual(passwordHashCode, userSecuritySchema.hashed_auth_token)

        # validate password
        saltHashCode, hashCode = HashUtils.hashCodeWithSalt(userSecuritySchema.hashed_auth_token,
                                                            userSecuritySchema.salt)
        logger.debug(f"saltHashCode={saltHashCode}, hashCode={hashCode}")
        self.assertTrue(HashUtils.checkHashCode(userSchema.password, saltHashCode, hashCode))

        logger.debug("-test_create_user_security()")
        print()

    def test_create_address(self):
        logger.debug("+test_create_address()")
        userEmail = super().getTestEmail()
        userName = userEmail.split("@")[0]
        userSchema = UserSchema(email=userEmail, first_name="Roh", last_name="Lak", birth_date="2024-12-27",
                                user_name=userName, password="password")
        logger.debug(f"userSchema={userSchema}")
        userSchema = self.userRepository.save(userSchema)
        logger.debug(f"userSchema={userSchema}")
        self.assertIsNotNone(userSchema.id)
        self.assertEqual(False, userSchema.admin)

        address_json = {
            "street1": "123 Test Dr.",
            "city": "Hayward",
            "state": "California",
            "country": "United States",
            "zip": "94544"
        }

        addressSchema = AddressSchema(**address_json)
        logger.debug(f"addressSchema={addressSchema}")
        userSchema.addresses.append(addressSchema)
        addressSchema = self.addressRepository.save(addressSchema)
        logger.debug(f"addressSchema={addressSchema}")
        self.assertIsNotNone(addressSchema.id)
        self.assertEqual("123 Test Dr.", addressSchema.street1)
        self.assertEqual("Hayward", addressSchema.city)
        self.assertEqual("California", addressSchema.state)
        self.assertEqual("United States", addressSchema.country)
        self.assertEqual("94544", addressSchema.zip)
        logger.debug("-test_create_address()")
        print()

    def assertAddressSchema(self, expected: AddressSchema, actual: AddressSchema):
        """Asserts the schema and model objects."""
        logger.debug(f"assertAddressSchema(), expected={expected}, actual={actual}")
        self.assertEqual(expected.id, actual.id)
        self.assertEqual(expected.street1, actual.street1)
        self.assertEqual(expected.city, actual.city)
        self.assertEqual(expected.state, actual.state)
        self.assertEqual(expected.country, actual.country)
        self.assertEqual(expected.zip, actual.zip)

    def test_create_user_with_address(self):
        logger.debug("+test_create_user_with_address()")
        userEmail = super().getTestEmail(True)
        userName = userEmail.split("@")[0]
        userSchema = UserSchema(email=userEmail, first_name="Roh", last_name="Lak", birth_date="2024-12-27",
                                admin=True, user_name=userName, password="password")
        logger.debug(f"userSchema={userSchema}")
        addressSchema = AddressSchema(street1="123 Test Dr.", city="Hayward", state="California",
                                      country="United States", zip="94544")
        logger.debug(f"addressSchema={addressSchema}")
        # assign address to user
        userSchema.addresses.append(addressSchema)
        userSchema = self.userRepository.save(userSchema)
        logger.debug(f"userSchema={userSchema}")
        self.assertIsNotNone(userSchema.id)
        self.assertEqual(True, userSchema.admin)

        # find user and validate
        adminUserSchema = self.userRepository.filter({"email": userEmail})[0]
        logger.debug(f"adminUserSchema={adminUserSchema}")
        self.assertIsNotNone(adminUserSchema.id)
        self.assertIsNotNone(adminUserSchema.addresses)
        self.assertEqual(1, len(adminUserSchema.addresses))
        self.assertAddressSchema(userSchema.addresses[0], adminUserSchema.addresses[0])

        logger.debug("-test_create_user_with_address()")
        print()


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
