#
# Author: Rohtash Lakra
#

import logging
import unittest

from rest.role.schema import RoleSchema
from rest.user.schema import UserSchema, AddressSchema
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class SqlAlchemyTest(AbstractTestCase):
    """Unit-tests for sqlalchemy"""

    def test_default_json_encoder(self):
        logger.debug("test_default_json_encoder")
        roleSchema = RoleSchema(name="TestRole", active=True)
        # jsonInstance = json.dumps(roleSchema, cls=sql_alchemy_encoder(), check_circular=False)
        # role_json = json.dumps(roleSchema, cls=DefaultJSONEncoder)
        expected = {'active': True, 'meta_data': None, 'name': 'TestRole', 'id': None, 'created_at': None,
                    'updated_at': None}
        roleJSONObject = roleSchema.toJSONObject()
        self.assertIsNotNone(roleJSONObject)
        logger.debug(f"roleSchema={roleSchema}, roleJSONObject={roleJSONObject}")
        self.assertEqual(expected, roleJSONObject)
        print()

    def test_recursive_encoder(self):
        logger.debug(f"+test_recursive_encoder()")
        address = AddressSchema(
            street1="123 Great Rd",
            city="Hayward",
            state="California",
            country="US",
            zip="94544"
        )

        self.assertIsNotNone(address)
        # address_json = json.dumps(address, cls=RecursiveJSONEncoder)
        # logger.debug(f"address={address}, address_json={address_json}")
        # self.assertIsNotNone(address_json)

        user = UserSchema(
            user_name="roh@lakra.com",
            password="Roh",
            email="roh@lakra.com",
            first_name="Rohtash",
            last_name="Lakra",
            admin=True,
            addresses=[address],
        )

        self.assertIsNotNone(user)
        # user_json = json.dumps(user, cls=RecursiveJSONEncoder)
        # logger.debug(f"user={user}, user_json={user_json}")
        # self.assertIsNotNone(user_json)

        logger.debug(f"-test_recursive_encoder()")
        print()

    def test_to_json(self):
        logger.debug(f"+test_to_json()")
        user = UserSchema(
            user_name="roh@lakra.com",
            password="Roh",
            email="roh@lakra.com",
            first_name="Rohtash",
            last_name="Lakra",
            admin=True,
            # birth_date=datetime.now(),
            # last_seen=datetime.now(),
            addresses=[]
        )

        self.assertIsNotNone(user)

        expected = {'user_name': 'roh@lakra.com', 'admin': True, 'last_seen': None,
                    'avatar_url': None, 'email': 'roh@lakra.com', 'first_name': 'Rohtash', 'last_name': 'Lakra',
                    'birth_date': None, 'id': None, 'created_at': None, 'updated_at': None}

        user_json = user.to_json()
        self.assertIsNotNone(user_json)
        logger.debug(f"user={user}, user_json={user_json}")
        self.assertEqual(expected, user_json)
        print()

        userJSONObject = user.toJSONObject()
        self.assertIsNotNone(userJSONObject)
        logger.debug(f"user={user}, userJSONObject={userJSONObject}")
        self.assertEqual(expected, userJSONObject)

        logger.debug(f"-test_to_json()")
        print()

    def test_toJSONObject(self):
        logger.debug(f"+test_toJSONObject()")
        address = AddressSchema(
            street1="123 Great Rd",
            city="Hayward",
            state="California",
            country="US",
            zip="94544"
        )

        self.assertIsNotNone(address)

        expected = {'user_id': None, 'street1': '123 Great Rd', 'street2': None, 'city': 'Hayward',
                    'state': 'California', 'country': 'US', 'zip': '94544', 'id': None, 'created_at': None,
                    'updated_at': None}
        addressJSONObject = address.toJSONObject()
        self.assertIsNotNone(addressJSONObject)
        logger.debug(f"address={address}, addressJSONObject={addressJSONObject}")
        self.assertEqual(expected, addressJSONObject)
        print()

        user = UserSchema(
            user_name="roh@lakra.com",
            password="Roh",
            email="roh@lakra.com",
            first_name="Rohtash",
            last_name="Lakra",
            admin=True,
            addresses=[address],
        )

        self.assertIsNotNone(user)

        expected = {'user_name': 'roh@lakra.com', 'admin': True, 'last_seen': None,
                    'avatar_url': None, 'email': 'roh@lakra.com', 'first_name': 'Rohtash', 'last_name': 'Lakra',
                    'birth_date': None, 'id': None, 'created_at': None, 'updated_at': None}

        userJSONObject = user.toJSONObject()
        self.assertIsNotNone(userJSONObject)
        logger.debug(f"user={user}, userJSONObject={userJSONObject}")
        self.assertEqual(expected, userJSONObject)
        logger.debug(f"-test_toJSONObject()")
        print()


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
