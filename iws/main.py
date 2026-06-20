#
# Author: Rohtash Lakra
#

import logging

import uvicorn
from dotenv import (load_dotenv, find_dotenv)
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from framework.logger import setup_logger
from globals import connector
from api.routes import api_router
from middleware import RequestIDMiddleware, lifespan, add_process_time_header
from rest import bp as rest_bp
from settings import ConfigSetting
from webapp.routes import webapp_router

# Ensure FastAPI runtime uses project logging config.
setup_logger()
logger = logging.getLogger(__name__)
# Load local environment variables from .env for development/runtime config.
load_dotenv(find_dotenv(".env"))


# Build the FastAPI app and delegate startup/shutdown to shared lifespan hooks.
app = FastAPI(
    redirect_slashes=True,
    docs_url="/docs",
    lifespan=lifespan,
)
# Attach request-scoped id middleware for per-request tracing.
app.add_middleware(RequestIDMiddleware)
# Attach HTTP middleware for request logging + X-Process-Time header.
app.middleware("http")(add_process_time_header)


# use custom logger adapter
# app.logger = DefaultLogger(app)
# app.logger.logConfig()
# Load typed runtime settings and initialize DB connector from those values.
configSettings = ConfigSetting()
logger.debug(f"configSettings={configSettings}")
logger.debug(f"configSettings dump={configSettings.model_dump()}")
# Initialize DB/session infrastructure before serving requests.
connector.init_db(app, configSettings.model_dump())
# Register API/UI route groups.
app.include_router(api_router)
app.include_router(rest_bp)
app.include_router(webapp_router)


# Serve static assets used by templates (css/js/images).
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")


if __name__ == '__main__':
    # Local entrypoint for direct python execution.
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=8082
    )
