#
# Author: Rohtash Lakra
#
from framework.orm.pydantic.entity import AbstractEntity
from tests.base import AbstractTestCase
from account.entity import User


class TestModel(AbstractTestCase):

    def test_user(self):
        """Tests the User entity"""
        print("+test_user()")
        user = User(100, "rlakra", "password", "Roh", "Lakra", "lakra@lakra.com")
        print(f"user: {user}")

        # valid object and expected results
        self.assertEqual(100, user.get_id())
        self.assertEqual("rlakra", user.user_name)
        self.assertFalse(user.admin)

        self.assertTrue(isinstance(user, AbstractEntity))
        self.assertFalse(isinstance(user, TestModel))
        self.assertTrue(issubclass(AbstractEntity, object))
        self.assertFalse(issubclass(object, AbstractEntity))

        print(f"user_json: \n{user.json()}")
        print("-test_user()")

    def test_admin_user(self):
        """Tests the User entity"""
        print("+test_admin_user()")
        user = User(200, "rslakra", "password", "Roh", "Lakra", "lakra@lakra.com", True)
        print(f"user: {user}")

        # valid object and expected results
        self.assertEqual(200, user.get_id())
        self.assertEqual("rslakra", user.user_name)
        self.assertTrue(user.admin)

        self.assertTrue(isinstance(user, AbstractEntity))
        self.assertFalse(isinstance(user, TestModel))
        self.assertTrue(issubclass(AbstractEntity, object))
        self.assertFalse(issubclass(object, AbstractEntity))

        print(f"user_json: \n{user.json()}")

        print("-test_admin_user()")
