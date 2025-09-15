#
# Author: Rohtash Lakra
#
import logging

from framework.security.hash import HashUtils
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class HashUtilsTest(AbstractTestCase):
    """Unit-tests for HashUtils class."""

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

    def test_hashDigestAndBase64(self):
        logger.debug("+test_hashDigestAndBase64()")
        rawText = "Password"
        expectedHashDigest = b'\xe7\xcf>\xf4\xf1|9\x99\xa9O,oa.\x8a\x88\x8e[\x10&\x87\x8eN\x199\x8b#\xbd8\xec"\x1a'
        expectedHashCode = "e7cf3ef4f17c3999a94f2c6f612e8a888e5b1026878e4e19398b23bd38ec221a"
        hashDigest, hashCode = HashUtils.hashDigestAndBase64(rawText)
        logger.debug(f"rawText={rawText}, hashDigest={hashDigest}, hashCode={hashCode}")
        self.assertEqual(expectedHashDigest, hashDigest)
        self.assertEqual(expectedHashCode, hashCode)
        logger.debug("-test_hashDigestAndBase64()")
        print()

    def test_hashCode(self):
        logger.debug("+test_hashCode()")
        rawText = "Password"
        expectedHashCode = "e7cf3ef4f17c3999a94f2c6f612e8a888e5b1026878e4e19398b23bd38ec221a"
        passwordHashCode = HashUtils.hashCode(rawText)
        logger.debug(f"rawText={rawText}, passwordHashCode={passwordHashCode}")
        self.assertEqual(expectedHashCode, passwordHashCode)
        logger.debug("-test_hashCode()")
        print()

    def test_hashCodeWithSalt(self):
        logger.debug("+test_hashCodeWithSalt()")
        rawText = "Password"
        expectedPasswordHashCode = "e7cf3ef4f17c3999a94f2c6f612e8a888e5b1026878e4e19398b23bd38ec221a"
        passwordHashCode = HashUtils.hashCode(rawText)
        logger.debug(f"rawText={rawText}, passwordHashCode={passwordHashCode}")
        self.assertEqual(expectedPasswordHashCode, passwordHashCode)

        salt = 'e3254be6fcc8492185d92843c5a3b2ba'
        logger.debug(f"salt={salt}")
        expectedSaltHashCode = "6533323534626536666363383439323138356439323834336335613362326261"
        expectedHashCode = "e7cf3ef4f17c3999a94f2c6f612e8a888e5b1026878e4e19398b23bd38ec221afd83f50845f78247470102206463ca5512e5ddbc438d20ec78cd15174242f654"
        saltHashCode, hashCode = HashUtils.hashCodeWithSalt(passwordHashCode, salt)
        logger.debug(f"saltHashCode={saltHashCode}, hashCode={hashCode}")
        self.assertEqual(expectedSaltHashCode, saltHashCode)
        self.assertEqual(expectedHashCode, hashCode)
        logger.debug("-test_hashCodeWithSalt()")
        print()

    def test_checkHashCode(self):
        logger.debug("+test_checkHashCode()")
        rawText = "Password"
        expectedPasswordHashCode = "e7cf3ef4f17c3999a94f2c6f612e8a888e5b1026878e4e19398b23bd38ec221a"
        passwordHashCode = HashUtils.hashCode(rawText)
        logger.debug(f"rawText={rawText}, passwordHashCode={passwordHashCode}")
        self.assertEqual(expectedPasswordHashCode, passwordHashCode)

        salt = 'e3254be6fcc8492185d92843c5a3b2ba'
        logger.debug(f"salt={salt}")
        expectedSaltHashCode = "6533323534626536666363383439323138356439323834336335613362326261"
        expectedHashCode = "e7cf3ef4f17c3999a94f2c6f612e8a888e5b1026878e4e19398b23bd38ec221afd83f50845f78247470102206463ca5512e5ddbc438d20ec78cd15174242f654"
        saltHashCode, hashCode = HashUtils.hashCodeWithSalt(passwordHashCode, salt)
        logger.debug(f"saltHashCode={saltHashCode}, hashCode={hashCode}")
        self.assertEqual(expectedSaltHashCode, saltHashCode)
        self.assertEqual(expectedHashCode, hashCode)

        self.assertTrue(HashUtils.checkHashCode(rawText, saltHashCode, hashCode))

        logger.debug("-test_checkHashCode()")
        print()
