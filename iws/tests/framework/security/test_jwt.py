#
# Author: Rohtash Lakra
#
import logging

from framework.security.jwt import AuthModel
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class JWTTest(AbstractTestCase):
    """Unit-tests for JWT classes."""

    def setUp(self):
        """The setUp() method of the TestCase class is automatically invoked before each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+setUp()")
        super().setUp()
        logger.debug("-setUp()")
        print()

    def tearDown(self):
        """The tearDown() method of the TestCase class is automatically invoked after each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+tearDown()")
        super().tearDown()
        logger.debug("-tearDown()")
        print()

    def test_create_AuthModel(self):
        logger.debug("+test_create_AuthModel()")
        json_object = {"user_id": 16, "auth_token": "password", "iat": 1736962330}
        authModel = AuthModel(**json_object)
        logger.debug(f"authModel={authModel}")
        self.assertIsNotNone(authModel)
        self.assertEqual(16, authModel.user_id)
        self.assertEqual("password", authModel.auth_token)
        self.assertEqual(1736962330, authModel.iat)
        logger.debug("-test_create_AuthModel()")
        print()
