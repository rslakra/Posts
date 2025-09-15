#
# Author: Rohtash Lakra
#
import json
import logging

from framework.orm.sqlalchemy.schema import BaseSchema
from rest.contact.schema import ContactSchema
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class ContactSchemaTest(AbstractTestCase):

    def setUp(self):
        """The setUp() method of the TestCase class is automatically invoked before each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+setUp()")
        super().setUp()

        # toString() test
        expected = "<class 'rest.contact.schema.ContactSchema'>"
        self.assertEqual(expected, str(ContactSchema))

        # init contact's schema object
        jsonContactSchema = {
            "first_name": "Roh",
            "last_name": "Lak",
            "country": "India",
            "subject": "Testing Contact's Schema"
        }

        self.contactSchema = ContactSchema(**jsonContactSchema)
        logger.debug(f"contactSchema={self.contactSchema}")
        self.assertIsNotNone(self.contactSchema)
        self.assertEqual("Roh", self.contactSchema.first_name)
        self.assertEqual("Lak", self.contactSchema.last_name)
        self.assertEqual("India", self.contactSchema.country)
        self.assertEqual("Testing Contact's Schema", self.contactSchema.subject)

        logger.debug("-setUp()")
        print()

    def tearDown(self):
        """The tearDown() method of the TestCase class is automatically invoked after each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+tearDown()")
        self.contactSchema = None
        self.assertIsNone(self.contactSchema)
        super().tearDown()
        logger.debug("-tearDown()")
        print()
        print()

    def assertContactSchema(self, expected: ContactSchema, actual: ContactSchema):
        """Asserts the contact's schema objects."""
        logger.debug(f"expected={expected}")
        logger.debug(f"actual={actual}")
        self.assertEqual(expected.id, actual.id)
        self.assertEqual(expected.first_name, actual.first_name)
        self.assertEqual(expected.last_name, actual.last_name)
        self.assertEqual(expected.country, actual.country)
        self.assertEqual(expected.subject, actual.subject)
        self.assertEqual(str(expected), str(actual))

    def test_contactSchema_isinstance_and_issubclass(self):
        """Tests the Model object"""
        logger.debug("+test_contactSchema_isinstance_and_issubclass()")
        logger.debug(f"contactSchema={self.contactSchema}")
        self.assertIsNotNone(self.contactSchema)

        # valid object and expected results
        self.assertTrue(isinstance(self.contactSchema, BaseSchema))
        self.assertFalse(isinstance(self.contactSchema, AbstractTestCase))
        self.assertTrue(issubclass(ContactSchema, object))
        self.assertFalse(issubclass(object, ContactSchema))
        logger.debug("-test_contactSchema_isinstance_and_issubclass()")
        print()

    def test_create_contactSchema(self):
        logger.debug("+test_create_contactSchema()")
        contactSchema = ContactSchema(first_name="First", last_name="Last", country="India")
        logger.debug(f"contactSchema={contactSchema}")
        self.assertIsNotNone(contactSchema)
        self.assertIsNone(contactSchema.id)
        self.assertEqual("First", contactSchema.first_name)
        self.assertEqual("Last", contactSchema.last_name)
        self.assertEqual("India", contactSchema.country)
        self.assertIsNone(contactSchema.subject)
        logger.debug("-test_create_contactSchema()")
        print()

    def test_contactSchema_to_json(self):
        logger.debug("+test_contactSchema_to_json()")
        logger.debug(f"contactSchema={self.contactSchema}")
        self.assertIsNotNone(self.contactSchema)

        contactSchema_json = json.dumps(self.contactSchema.to_json())
        logger.debug(f"contactSchema_json={contactSchema_json}")
        self.assertIsNotNone(contactSchema_json)

        jsonContactSchema = json.loads(contactSchema_json)
        logger.debug(f"jsonContactSchema={jsonContactSchema}")

        contactSchema = ContactSchema(**jsonContactSchema)
        self.assertContactSchema(self.contactSchema, contactSchema)
        logger.debug("-test_contactSchema_to_json()")
        print()
