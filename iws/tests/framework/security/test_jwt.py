#
# Author: Rohtash Lakra
#
import logging

from framework.security.jwt import AuthModel, TokenManager
from framework.utils import Utils
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
    
    def test_token_manager(self):
        logger.debug("+test_token_manager()")
        userId = Utils.randomUUID()
        clientSecret = "a79387fed978428e9ced80fb1db9125d"
        
        token_manager = TokenManager(userId, clientSecret)
        logger.debug(f"token_manager={token_manager}")
        self.assertIsNotNone(token_manager)
        token = token_manager.getAccessToken(userId)
        logger.debug(f"token={token}")
        self.assertIsNotNone(token_manager)
        self.assertEqual(userId, token.userId)
        self.assertIsNotNone(token.refreshToken)
        self.assertIsNotNone(token.accessToken)
        self.assertIsNotNone(token.expiresAt)
        logger.debug("-test_token_manager()")
        print()
    
    def test_getAccessToken(self):
        logger.debug("+test_getAccessToken()")
        userId = Utils.randomUUID()
        clientSecret = "a79387fed978428e9ced80fb1db9125d"
        
        token_manager = TokenManager(userId, clientSecret)
        logger.debug(f"token_manager={token_manager}")
        self.assertIsNotNone(token_manager)
        token = token_manager.getAccessToken(userId)
        logger.debug(f"token={token}")
        self.assertIsNotNone(token_manager)
        self.assertEqual(userId, token.userId)
        self.assertIsNotNone(token.refreshToken)
        self.assertIsNotNone(token.accessToken)
        self.assertIsNotNone(token.expiresAt)
        logger.debug("-test_getAccessToken()")
        print()
    
    def test_refreshAccessToken(self):
        logger.debug("+test_refreshAccessToken()")
        userId = Utils.randomUUID()
        clientSecret = "a79387fed978428e9ced80fb1db9125d"
        
        token_manager = TokenManager(userId, clientSecret)
        logger.debug(f"token_manager={token_manager}")
        self.assertIsNotNone(token_manager)
        token = token_manager.getAccessToken(userId)
        logger.debug(f"token={token}")
        self.assertIsNotNone(token_manager)
        self.assertEqual(userId, token.userId)
        self.assertIsNotNone(token.refreshToken)
        self.assertIsNotNone(token.accessToken)
        self.assertIsNotNone(token.expiresAt)
        
        refreshToken = token.refreshToken
        token = token_manager.refreshAccessToken(userId, token)
        logger.debug(f"new access_token={token}")
        self.assertIsNotNone(token_manager)
        self.assertEqual(userId, token.userId)
        self.assertIsNotNone(token.refreshToken)
        self.assertEqual(refreshToken, token.refreshToken)
        self.assertIsNotNone(token.accessToken)
        self.assertIsNotNone(token.expiresAt)
        logger.debug("-test_refreshAccessToken()")
        print()
