#
# Author: Rohtash Lakra
#
import logging

from framework.http import HTTPMethod, HTTPStatus, HTTPUtils
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class HttpTest(AbstractTestCase):
    
    def test_http_method(self):
        logger.debug("test_http_method()")
        http_method = HTTPMethod.GET
        logger.debug(f"http_method={http_method}")
        self.assertEqual(HTTPMethod.GET, http_method)
        self.assertNotEqual(HTTPMethod.POST, http_method)
        
        expected = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')
        self.assertEqual("<enum 'HTTPMethod'>", str(HTTPMethod))
        self.assertEqual(expected, HTTPMethod.names())
        self.assertEqual(expected, HTTPMethod.values())
        
        text = 'get'
        expected = 'HTTPMethod <GET=GET>'
        logger.debug(f"{text} of_name={HTTPMethod.of_name(text)}")
        self.assertEqual(expected, str(HTTPMethod.of_name(text)))
        self.assertTrue(HTTPMethod.equals(HTTPMethod.GET, text))
        
        text = 'post'
        logger.debug(f"{text} of_value={HTTPMethod.of_value(text)}")
        self.assertIsNone(HTTPMethod.of_value(text))
    
    def test_is_post(self):
        logger.debug("test_is_post()")
        self.assertTrue(HTTPMethod.is_post("post"))
        self.assertTrue(HTTPMethod.is_post("Post"))
        self.assertTrue(HTTPMethod.is_post("POST"))
        self.assertTrue(HTTPMethod.is_post("PoST"))
        self.assertFalse(HTTPMethod.is_post("get"))
    
    def test_http_status(self):
        logger.debug("test_http_status()")
        httpStatus = HTTPStatus.CREATED
        logger.debug(f"httpStatus={httpStatus}")
        self.assertEqual(HTTPStatus.CREATED, httpStatus)
        self.assertNotEqual(HTTPStatus.OK, httpStatus)
        
        expected = "HTTPStatus <CREATED=(201, 'Created')>"
        self.assertEqual(expected, str(httpStatus))
        self.assertEqual("<enum 'HTTPStatus'>", str(HTTPStatus))
        
        logger.debug(f"HTTPStatus names={HTTPStatus.names()}")
        expected = ('OK', 'CREATED', 'ACCEPTED', 'NO_CONTENT', 'BAD_REQUEST', 'UNAUTHORIZED', 'NOT_FOUND', 'CONFLICT',
                    'UNSUPPORTED_MEDIA_TYPE', 'INVALID_DATA', 'TOO_MANY_REQUESTS', 'INTERNAL_SERVER_ERROR',
                    'NOT_IMPLEMENTED', 'SERVICE_UNAVAILABLE', 'GATEWAY_TIMEOUT')
        self.assertEqual(expected, HTTPStatus.names())
        
        logger.debug(f"HTTPStatus values={HTTPStatus.values()}")
        expected = ((200, 'OK'), (201, 'Created'), (202, 'Accepted'), (204, 'No Content'), (400, 'Bad Request'),
                    (401, 'Unauthorized'), (404, 'Not Found'), (409, 'Conflict'), (415, 'Unsupported Media Type'),
                    (422, 'Unprocessable Entity'), (429, 'Too Many Requests'), (500, 'Internal Server Error'),
                    (501, 'Not Implemented'), (503, 'Service Unavailable'), (504, 'Gateway Timeout'))
        self.assertEqual(expected, HTTPStatus.values())
        
        text = 'ok'
        expected = "HTTPStatus <OK=(200, 'OK')>"
        logger.debug(f"{text} of_name={HTTPStatus.of_name(text)}")
        self.assertEqual(expected, str(HTTPStatus.of_name(text)))
        self.assertTrue(HTTPStatus.equals(HTTPStatus.OK, text))
    
    def test_fromStatus(self):
        logger.debug("test_fromStatus()")
        self.assertEqual(HTTPStatus.OK, HTTPStatus.fromStatus(200))
        self.assertEqual(HTTPStatus.CREATED, HTTPStatus.fromStatus(201))
        self.assertEqual(HTTPStatus.BAD_REQUEST, HTTPStatus.fromStatus(400))
        self.assertEqual(HTTPStatus.UNAUTHORIZED, HTTPStatus.fromStatus(401))
        self.assertEqual(HTTPStatus.NOT_FOUND, HTTPStatus.fromStatus(404))
        self.assertEqual(HTTPStatus.TOO_MANY_REQUESTS, HTTPStatus.fromStatus(429))
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.fromStatus(500))
    
    def test_getSuccessStatuses(self):
        logger.debug("+test_getSuccessStatuses()")
        expected = '[OK <200, OK, None>, CREATED <201, Created, None>, ACCEPTED <202, Accepted, None>, NO_CONTENT <204, No Content, None>]'
        success_statuses = HTTPStatus.getSuccessStatuses()
        logger.debug(f"success_statuses={success_statuses}")
        self.assertEqual(expected, str(success_statuses))
        self.assertNotEqual(['UNAUTHORIZED <401, Unauthorized>'], str(success_statuses))
        logger.debug("-test_getSuccessStatuses()")
        print()
    
    def test_is_success_status(self):
        logger.debug("test_is_success_status()")
        self.assertTrue(HTTPStatus.isStatusSuccess(HTTPStatus.OK))
        self.assertTrue(HTTPStatus.isStatusSuccess(HTTPStatus.CREATED))
        self.assertTrue(HTTPStatus.isStatusSuccess(HTTPStatus.ACCEPTED))
        self.assertTrue(HTTPStatus.isStatusSuccess(HTTPStatus.NO_CONTENT))
        self.assertFalse(HTTPStatus.isStatusSuccess(HTTPStatus.BAD_REQUEST))
    
    def test_get(self):
        logger.debug("test_get()")
        http = HTTPUtils()
        logger.debug(f"http={http}")
        url = http.get("/posts")
        logger.debug(f"url={url}")
        self.assertIsNotNone(url)
        self.assertEqual('GET /posts', url)
    
    def test_post(self):
        logger.debug("test_post()")
        http = HTTPUtils()
        logger.debug(f"http={http}")
        url = http.post("/posts")
        logger.debug(f"url={url}")
        self.assertIsNotNone(url)
        self.assertEqual('POST /posts', url)
