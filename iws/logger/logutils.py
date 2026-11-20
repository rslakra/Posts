#
# Author: Rohtash Lakra
# References:
#  - https://blog.mcpolemic.com/2016/01/18/adding-request-ids-to-flask.html
import logging
import uuid
from contextvars import ContextVar
from typing import Optional

"""
Request IDs

A request ID is a unique identifier for each request. We decided that we wanted to be able to search for both a unique 
action and an entire request chain, so we implemented the following model:

- If a request comes in with no request ID, generate a unique one.
- If a request comes in with a request ID, add a comma and add a unique one.

This allows the requests chain (which could have any number of requests in between them) to  handle easily.

The request id is stored in a `ContextVar` (the ASGI/FastAPI replacement of Flask's `g`), which is set per request by
a middleware (see `logger/server.py`).
"""

# holds the id of the request that is being served by the current context.
request_id_context: ContextVar[Optional[str]] = ContextVar("request_id", default=None)


def generate_request_id(original_request_id: str = '') -> str:
    """Generate a new request ID, optionally including an original request ID"""
    request_id = uuid.uuid4().hex

    if original_request_id:
        request_id = "{}, {}".format(original_request_id, request_id)

    return request_id


class RequestIdFilter(logging.Filter):
    """RequestIdFilter class"""

    # This is a logging filter that makes the request ID available for use in the logging format. Outside of a
    # request (e.g. while the application is starting) the request id is empty.
    def filter(self, record):
        record.request_id = request_id_context.get() or ''
        return True

    def _generate_request_id(self, original_request_id=''):
        """Generate a new request ID, optionally including an original request ID"""
        return generate_request_id(original_request_id)

    def print_reqeust_id(self):
        """Prints request id"""
        print()
        requestId = self._generate_request_id()
        print(f"requestId: {requestId}")
        print(f"Next requestId: {self._generate_request_id(requestId)}")
        print(f"Last requestId: {self._generate_request_id(requestId)}")
        print()


# Uncomment to test it.
# reqeustIdFilter = RequestIdFilter()
# reqeustIdFilter.print_reqeust_id()
