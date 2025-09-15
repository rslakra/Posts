#
# Author: Rohtash Lakra
#
import json
import logging

from framework.http import HTTPStatus
from framework.orm.pydantic.model import AbstractModel, ResponseModel, ErrorModel
from rest.contact.model import Contact
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class ContactModelTest(AbstractTestCase):

    def setUp(self):
        """The setUp() method of the TestCase class is automatically invoked before each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+setUp()")
        super().setUp()

        # toString() test
        expected = "<class 'rest.contact.model.Contact'>"
        self.assertEqual(expected, str(Contact))

        # init object
        self.contact = Contact(id=16, first_name="Roh", last_name="Lak", country="India", subject="Contact's Object")
        logger.debug(f"contact={self.contact}")
        self.assertIsNotNone(self.contact)
        self.assertEqual(16, self.contact.id)
        self.assertEqual("Roh", self.contact.first_name)
        self.assertEqual("Lak", self.contact.last_name)
        self.assertEqual("India", self.contact.country)
        self.assertEqual("Contact's Object", self.contact.subject)

        logger.debug("-setUp()")
        print()

    def tearDown(self):
        """The tearDown() method of the TestCase class is automatically invoked after each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+tearDown()")
        self.contact = None
        self.assertIsNone(self.contact)
        super().tearDown()
        logger.debug("-tearDown()")
        print()

    def assertContact(self, expected: Contact, actual: Contact):
        # valid object and expected results
        self.assertEqual(expected, actual)
        self.assertEqual(expected.id, actual.id)
        self.assertEqual(expected.first_name, actual.first_name)
        self.assertEqual(expected.last_name, actual.last_name)
        self.assertEqual(expected.country, actual.country)
        self.assertEqual(expected.subject, actual.subject)

    def test_contact_isinstance_and_issubclass(self):
        """Tests the Model object"""
        logger.debug("+test_contact_isinstance_and_issubclass()")
        logger.debug(f"contact={self.contact}")
        self.assertIsNotNone(self.contact)
        # valid object and expected results
        self.assertTrue(isinstance(self.contact, AbstractModel))
        self.assertFalse(isinstance(self.contact, AbstractTestCase))
        self.assertTrue(issubclass(Contact, object))
        self.assertFalse(issubclass(object, Contact))
        logger.debug("-test_contact_isinstance_and_issubclass()")
        print()

    def test_create_contact(self):
        logger.debug("+test_create_contact()")
        self.contact = Contact(first_name="First", last_name="Last", country="India")
        logger.debug(f"contact={self.contact}")
        self.assertIsNotNone(self.contact)
        self.assertIsNone(self.contact.id)
        self.assertEqual("First", self.contact.first_name)
        self.assertEqual("Last", self.contact.last_name)
        self.assertEqual("India", self.contact.country)
        self.assertIsNone(self.contact.subject)
        logger.debug("-test_create_contact()")
        print()

    def test_contact_to_json(self):
        logger.debug("+test_contact_to_json()")
        logger.debug(f"contact={self.contact}")
        self.assertIsNotNone(self.contact)

        contact_json = self.contact.to_json()
        logger.debug(f"contact_json={contact_json}")
        self.assertIsNotNone(contact_json)

        jsonContact = json.loads(contact_json)
        logger.debug(f"jsonContact={jsonContact}")

        contact = Contact(**jsonContact)
        self.assertContact(self.contact, contact)
        logger.debug("-test_contact_to_json()")
        print()

    def test_contact_created_response(self):
        """Tests an ResponseModel object"""
        logger.debug("+test_contact_created_response()")
        logger.debug(f"contact={self.contact}")
        self.assertIsNotNone(self.contact)

        response = ResponseModel.buildResponse(HTTPStatus.CREATED, self.contact)
        logger.debug(f"response={response}")
        self.assertIsNotNone(response)
        self.assertEqual(HTTPStatus.CREATED.statusCode, response.status)
        self.assertIsNotNone(response.data)
        self.assertIsNone(response.errors)
        self.assertFalse(response.hasError())

        response_json = response.to_json()
        logger.debug(f"response_json={response_json}")
        self.assertIsNotNone(response_json)

        # build json response
        jsonResponse = ResponseModel.jsonResponse(HTTPStatus.CREATED, self.contact)
        logger.debug(f"jsonResponse={jsonResponse}")
        self.assertIsNotNone(jsonResponse)
        self.assertEqual(jsonResponse, response_json)
        logger.debug("-test_contact_created_response()")
        print()

    def test_contact_bad_request_response(self):
        """Tests an ResponseModel object"""
        logger.debug("+test_contact_bad_request_response()")
        logger.debug(f"contact={self.contact}")
        self.assertIsNotNone(self.contact)

        response = ResponseModel.buildResponse(HTTPStatus.BAD_REQUEST, self.contact, message="Test Failure")
        logger.debug(f"response={response}")
        self.assertIsNotNone(response)
        self.assertEqual(HTTPStatus.BAD_REQUEST.statusCode, response.status)
        self.assertIsNone(response.data)
        self.assertTrue(response.hasError())
        self.assertIsNotNone(response.errors)
        self.assertTrue(len(response.errors) > 0)

        response_json = response.to_json()
        logger.debug(f"response_json={response_json}")
        self.assertIsNotNone(response_json)

        # build json response
        jsonResponse = ResponseModel.jsonResponse(HTTPStatus.BAD_REQUEST, self.contact, message="Test Failure")
        logger.debug(f"jsonResponse={jsonResponse}")
        self.assertIsNotNone(jsonResponse)
        self.assertEqual(jsonResponse, response_json)
        logger.debug("-test_contact_bad_request_response()")
        print()

    def test_create_response_model(self):
        """Tests an ResponseModel object"""
        logger.debug("+test_create_response_model()")
        logger.debug(f"contact={self.contact}")
        self.assertIsNotNone(self.contact)

        response = ResponseModel.buildResponse(HTTPStatus.BAD_REQUEST)
        logger.debug(f"response={response}")
        self.assertIsNotNone(response)
        # add contact's instance
        response.addInstance(self.contact)
        # add error's response
        allErrors = [ErrorModel.buildError(HTTPStatus.INVALID_DATA, message='First name should provide!'),
                     ErrorModel.buildError(HTTPStatus.INVALID_DATA, message='Last name should provide!')]
        response.addInstances(allErrors)
        logger.debug(f"response={response}")

        # assert instance
        self.assertEqual(HTTPStatus.BAD_REQUEST.statusCode, response.status)
        self.assertIsNotNone(response.data)
        self.assertTrue(response.hasError())
        self.assertIsNotNone(response.errors)
        self.assertTrue(len(response.errors) > 0)

        response_json = response.to_json()
        logger.debug(f"response_json={response_json}")
        self.assertIsNotNone(response_json)

        # build json response
        allInstances = allErrors.copy()
        allInstances.append(self.contact)
        jsonResponse = ResponseModel.jsonResponses(HTTPStatus.BAD_REQUEST, instances=allInstances)
        logger.debug(f"jsonResponse={jsonResponse}")
        self.assertIsNotNone(jsonResponse)
        self.assertEqual(jsonResponse, response_json)
        logger.debug("-test_create_response_model()")
        print()
