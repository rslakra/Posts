import logging
import unittest

from rest.contact.repository import ContactRepository
from rest.contact.schema import ContactSchema
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class ContactRepositoryTest(AbstractTestCase):
    """Unit-tests for Repository classes"""

    def setUp(self):
        """The setUp() method of the TestCase class is automatically invoked before each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+setUp()")
        super().setUp()

        # toString() test
        expected = "<class 'rest.contact.repository.ContactRepository'>"
        self.assertEqual(expected, str(ContactRepository))

        # init object
        self.contactRepository = ContactRepository()
        logger.debug(f"contactRepository={self.contactRepository}")
        self.assertIsNotNone(self.contactRepository)
        expected = 'ContactRepository <engine=Engine(sqlite:///testPosts.db)>'
        self.assertEqual(expected, str(self.contactRepository))
        self.assertIsNotNone(self.contactRepository.get_engine())

        logger.debug("-setUp()")
        print()

    def tearDown(self):
        """The tearDown() method of the TestCase class is automatically invoked after each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+tearDown()")
        self.contactRepository = None
        self.assertIsNone(self.contactRepository)
        super().tearDown()
        logger.debug("-tearDown()")
        print()

    def test_create_contact(self):
        logger.debug("+test_create_contact()")
        # contact
        contact_json = {
            "first_name": "Roh",
            "last_name": "Lak",
            "country": "India",
            "subject": "Testing Contact's Repository"
        }
        contactSchema = ContactSchema(**contact_json)
        logger.debug(f"contactSchema={contactSchema}")
        contactSchema = self.contactRepository.save(contactSchema)
        logger.debug(f"contactSchema={contactSchema}")
        self.assertIsNotNone(contactSchema.id)
        self.assertEqual("India", contactSchema.country)
        logger.debug("-test_create_contact()")
        print()


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
