#
# Author: Rohtash Lakra
# References:
#  - https://blog.mcpolemic.com/2016/01/18/adding-request-ids-to-flask.html
#
# Run (from the 'logger' directory): uvicorn server:app --port 5000
import logging

import log  # noqa: F401 (configures the logging format)
import uvicorn
from fastapi import FastAPI, Request

from logutils import generate_request_id, request_id_context

# set up a small FastAPI app to show it in action.
logger = logging.getLogger(__name__)
app = FastAPI()


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    """Sets the request id (chained with the incoming 'X-Request-Id' header, if any) for the current request."""
    request_id = generate_request_id(request.headers.get("X-Request-Id", ""))
    token = request_id_context.set(request_id)
    try:
        response = await call_next(request)
    finally:
        request_id_context.reset(token)

    response.headers["X-Request-Id"] = request_id
    return response


# route
# curl http://127.0.0.1:5000/
# curl --header 'X-Request-Id:cc4edc3c-ba0d-40c9-b76d-563f8fe08bd9' http://127.0.0.1:5000/
@app.get("/")
def hello():
    logger.info("Sending our hello")
    test_other()
    return "Hello World!"


def test_other():
    print("Starting test_other()")
    logger.info("Testing other method logging")
    print("Ending test_other()")


if __name__ == "__main__":
    uvicorn.run(app, port=5000)
