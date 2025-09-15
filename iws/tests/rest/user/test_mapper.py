import logging
import unittest

from rest.user.mapper import UserMapper, AddressMapper, UserSecurityMapper
from rest.user.model import User, Address, UserSecurity
from rest.user.schema import UserSchema, AddressSchema, UserSecuritySchema
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class UserMapperTest(AbstractTestCase):
    """Unit-tests for Mapper classes"""

    def test_user_mappers(self):
        logger.debug("+test_user_mappers()")
        expected = "<class 'rest.user.mapper.UserMapper'>"
        self.assertEqual(expected, str(UserMapper))

        expected = "<class 'rest.user.mapper.AddressMapper'>"
        self.assertEqual(expected, str(AddressMapper))
        logger.debug("-test_user_mappers()")
        print()

    def assertUserObjects(self, schemaObject: UserSchema, modelObject: User):
        """Asserts the schema and model objects."""
        logger.debug(f"assertUserObjects({schemaObject}, {modelObject})")
        self.assertEqual(schemaObject.id, modelObject.id)
        self.assertEqual(schemaObject.email, modelObject.email)
        self.assertEqual(schemaObject.first_name, modelObject.first_name)
        self.assertEqual(schemaObject.last_name, modelObject.last_name)
        self.assertEqual(schemaObject.birth_date, modelObject.birth_date)
        self.assertEqual(schemaObject.user_name, modelObject.user_name)
        self.assertEqual(schemaObject.admin, modelObject.admin)
        self.assertEqual(schemaObject.last_seen, modelObject.last_seen)
        self.assertEqual(schemaObject.avatar_url, modelObject.avatar_url)

    def test_user_fromSchema(self):
        logger.debug("+test_user_fromSchema()")
        # create a user
        userSchema = UserSchema(email="userSchema@lakra.com", first_name="Roh", last_name="Lak",
                                birth_date="2024-12-27",
                                user_name="userSchema", password="password")
        logger.debug(f"userSchema={userSchema}")
        self.assertIsNotNone(userSchema)
        userModel = UserMapper.fromSchema(userSchema)
        logger.debug(f"userModel={userModel}")
        self.assertIsNotNone(userModel)

        # validate objects
        self.assertUserObjects(userSchema, userModel)
        logger.debug("-test_user_fromSchema()")
        print()

    def test_user_fromModel(self):
        logger.debug("+test_user_fromModel()")
        # create a user
        userModel = User(email="userModel@lakra.com", first_name="Roh", last_name="Lak", birth_date="2024-12-27",
                         user_name="userModel", password="password")
        logger.debug(f"userModel={userModel}")
        self.assertIsNotNone(userModel)
        userSchema = UserMapper.fromModel(userModel)
        logger.debug(f"userSchema={userSchema}")
        self.assertIsNotNone(userSchema)

        # validate objects
        self.assertUserObjects(userSchema, userModel)
        logger.debug("-test_user_fromModel()")
        print()

    def assertUserSecurity(self, schemaObject: UserSecuritySchema, modelObject: UserSecurity):
        """Asserts the schema and model objects."""
        logger.debug(f"assertUserSecurity({schemaObject}, {modelObject})")
        self.assertEqual(schemaObject.user_id, modelObject.user_id)
        self.assertEqual(schemaObject.platform, modelObject.platform)
        self.assertEqual(schemaObject.salt, modelObject.salt)
        self.assertEqual(schemaObject.hashed_auth_token, modelObject.hashed_auth_token)
        self.assertEqual(schemaObject.expire_at, modelObject.expire_at)
        self.assertEqual(schemaObject.meta_data, modelObject.meta_data)

    def test_userSecurity_fromSchema(self):
        logger.debug("+test_userSecurity_fromSchema()")
        # userSecurity
        schemaObject = UserSecuritySchema(platform="Model", salt="Salt", hashed_auth_token="hashedAuthToken")
        logger.debug(f"schemaObject={schemaObject}")
        self.assertIsNotNone(schemaObject)
        # mapper
        modelObject = UserSecurityMapper.fromSchema(schemaObject)
        logger.debug(f"modelObject={modelObject}")
        self.assertIsNotNone(modelObject)
        # validate schema and model objects
        self.assertUserSecurity(schemaObject, modelObject)
        logger.debug("-test_userSecurity_fromSchema()")
        print()

    def test_userSecurity_fromModel(self):
        logger.debug("+test_userSecurity_fromModel()")
        # userSecurity
        modelObject = UserSecurity(platform="Model", salt="Salt", hashed_auth_token="hashedAuthToken")
        logger.debug(f"modelObject={modelObject}")
        self.assertIsNotNone(modelObject)
        # mapper
        schemaObject = UserSecurityMapper.fromModel(modelObject)
        logger.debug(f"schemaObject={schemaObject}")
        self.assertIsNotNone(schemaObject)
        # validate schema and model objects
        self.assertUserSecurity(schemaObject, modelObject)
        logger.debug("-test_userSecurity_fromModel()")
        print()

    def test_user_fromModel_with_userSecurity(self):
        logger.debug("+test_user_fromModel_with_userSecurity()")
        # userSecurity
        # Create user with address
        userModel = User(email="userModel@lakra.com", first_name="Roh", last_name="Lak", birth_date="2024-12-27",
                         user_name="userModel", password="password")
        logger.debug(f"userModel={userModel}")
        self.assertIsNotNone(userModel)

        userSecurityModel = UserSecurity(platform="Model", salt="Salt", hashed_auth_token="hashedAuthToken")
        logger.debug(f"userSecurityModel={userSecurityModel}")
        self.assertIsNotNone(userSecurityModel)
        userModel.user_security = userSecurityModel
        self.assertIsNotNone(userModel.user_security)
        # mapper
        userSchema = UserMapper.fromModel(userModel)
        logger.debug(f"userSchema={userSchema}")
        self.assertIsNotNone(userSchema)

        self.assertUserObjects(userSchema, userModel)
        self.assertIsNotNone(userSchema.user_security)
        self.assertIsNotNone(userModel.user_security)
        # asset user's security
        self.assertUserObjects(userSchema, userModel)
        logger.debug("-test_user_fromModel_with_userSecurity()")
        print()

    def assertAddressObjects(self, schemaObject: AddressSchema, modelObject: Address):
        """Asserts the schema and model objects."""
        logger.debug(f"assertAddressObjects({schemaObject}, {modelObject})")
        self.assertEqual(schemaObject.id, modelObject.id)
        self.assertEqual(schemaObject.street1, modelObject.street1)
        self.assertEqual(schemaObject.city, modelObject.city)
        self.assertEqual(schemaObject.state, modelObject.state)
        self.assertEqual(schemaObject.country, modelObject.country)
        self.assertEqual(schemaObject.zip, modelObject.zip)

    def test_address_fromSchema(self):
        logger.debug("+test_address_fromSchema()")
        # create an address
        addressSchema = AddressSchema(street1="123 Test Dr.", city="Hayward", state="California",
                                      country="United States", zip="94544")
        logger.debug(f"addressSchema={addressSchema}")
        self.assertIsNotNone(addressSchema)
        addressModel = AddressMapper.fromSchema(addressSchema)
        logger.debug(f"addressModel={addressModel}")
        self.assertIsNotNone(addressModel)

        # validate objects
        self.assertAddressObjects(addressSchema, addressModel)
        logger.debug("-test_address_fromSchema()")
        print()

    def test_address_fromModel(self):
        logger.debug("+test_address_fromModel()")
        # create an address
        addressModel = Address(street1="123 Test Dr.", city="Hayward", state="California",
                               country="United States", zip="94544")
        logger.debug(f"addressModel={addressModel}")
        self.assertIsNotNone(addressModel)
        addressSchema = AddressMapper.fromModel(addressModel)
        logger.debug(f"addressSchema={addressSchema}")
        self.assertIsNotNone(addressSchema)

        # validate objects
        self.assertAddressObjects(addressSchema, addressModel)
        logger.debug("-test_address_fromModel()")
        print()

    def test_user_fromModel_with_address(self):
        logger.debug("+test_user_fromModel_with_address()")
        # Create user with address
        userModel = User(email="userModel@lakra.com", first_name="Roh", last_name="Lak", birth_date="2024-12-27",
                         user_name="userModel", password="password")
        logger.debug(f"userModel={userModel}")
        self.assertIsNotNone(userModel)

        # create address
        addressModel = Address(street1="123 Test Dr.", city="Hayward", state="California",
                               country="United States", zip="94544")
        logger.debug(f"addressModel={addressModel}")
        self.assertIsNotNone(addressModel)
        # Assign address to user
        userModel.addresses.append(addressModel)
        logger.debug(f"userModel={userModel}")
        self.assertIsNotNone(userModel.addresses)

        userSchema = UserMapper.fromModel(userModel)
        logger.debug(f"userSchema={userSchema}")
        self.assertIsNotNone(userSchema)

        self.assertUserObjects(userSchema, userModel)
        self.assertIsNotNone(userSchema.addresses)
        self.assertIsNotNone(userModel.addresses)
        self.assertEqual(1, len(userSchema.addresses))
        self.assertEqual(1, len(userModel.addresses))

        # asset user's address
        self.assertAddressObjects(userSchema.addresses[0], addressModel)
        logger.debug("-test_user_fromModel_with_address()")
        print()


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
