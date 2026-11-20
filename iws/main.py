#
# Author: Rohtash Lakra
#

import logging

import uvicorn
from dotenv import (load_dotenv, find_dotenv)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import Config
from framework.logger import setup_logger
from globals import connector
from api import bp as api_bp
from api.routes import api_router
from handlers import registerExceptionHandlers
from middleware import RequestIDMiddleware, lifespan, add_process_time_header
from rest import bp as rest_bp
from settings import ENV_FILE, ConfigSetting
from webapp.routes import webapp_router

# Ensure FastAPI runtime uses project logging config.
setup_logger()
logger = logging.getLogger(__name__)
# Load local environment variables from the env file ('.env', or '.env.test' for tests) for development/runtime config.
load_dotenv(find_dotenv(ENV_FILE))


# Build the FastAPI app and delegate startup/shutdown to shared lifespan hooks.
app = FastAPI(
    redirect_slashes=True,
    docs_url="/docs",
    lifespan=lifespan,
)
# Enable CORS (all origins, same defaults as Flask-CORS) when CORS_ENABLED is set.
if Config.is_cors_enabled():
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
# Attach request-scoped id middleware for per-request tracing.
app.add_middleware(RequestIDMiddleware)
# Attach HTTP middleware for request logging + X-Process-Time header.
app.middleware("http")(add_process_time_header)
# Register JSON error handlers (HTTP errors, validation errors, application exceptions, unhandled errors).
registerExceptionHandlers(app)


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
app.include_router(api_bp)
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
