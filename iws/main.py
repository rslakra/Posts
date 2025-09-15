#
# Author: Rohtash Lakra
#

import logging
import time
from contextlib import asynccontextmanager
from functools import lru_cache
from typing import (
    AsyncIterator,
    List
)

import uvicorn
from dotenv import (load_dotenv, find_dotenv)
from fastapi import FastAPI, Depends, status, Request
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.types import Text

from framework.orm.pydantic.model import ConfigSetting
from globals import connector
from rest.contact.model import Contact
from rest.contact.service import ContactService

logger = logging.getLogger(__name__)
# load .dotenv settings.
load_dotenv(find_dotenv(".env"))


@lru_cache
def getSettings():
    return ConfigSetting()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # pylint: disable=redefined-outer-name
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """

    print('Startup')
    logger.info("Startup")
    logger.info("Validating DB connection on startup...")
    async with connector.connect() as conn:
        await conn.execute(Text("SELECT 1"))
        logger.info("Database connection validated during startup.")
    yield

    if connector.engine is not None:  # pylint: disable=protected-access
        await connector.close()
        logger.info("Database engine closed on shutdown.")

    logger.info("Shutdown")
    print('Shutdown')


# Initialize 'FastAPI' Application
app = FastAPI(
    redirect_slashes=False,
    docs_url="/docs",
)


@app.middleware("http")
async def add_process_time_header(request: Request, next_call):
    start_time = time.time()
    response = await next_call(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# use custom logger adapter
# app.logger = DefaultLogger(app)
# app.logger.logConfig()
# init configs
configSettings = getSettings()
logger.debug(f"configSettings={configSettings}")
logger.debug(f"configSettings dump={configSettings.model_dump()}")
# init connector
connector.init_db(app, configSettings.model_dump())


# app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> JSONResponse:
    """Endpoint to prevent 404 when loading the docs"""
    return FileResponse("webapp/static/images/webapp-logo.png")
    # return JSONResponse(status_code=204, content="")


@app.get("/health-check", tags=["Default Resources"], summary="Health Check", description="Returns Health Check Status")
async def healthCheck() -> JSONResponse:
    """The Health Check endpoint.
    Returns a default success message indicating the application is running.
    """
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "FastAPI ./v2/health-check"})


@app.get("/info", tags=["Default Resources"], summary="Get Configs", description="Get '.env' Configs")
async def info(config: ConfigSetting = Depends(getSettings)):
    return config.model_dump()


class ContactCreate(Contact):
    pass


@app.post(
    "/contacts",
    tags=["Contacts"],
    summary="Create Contact",
    description="Creates a new contact",
    response_model=Contact
)
def createContact(contact: Contact, session: Session = Depends(connector.getSession)):
    contactService = ContactService()
    contact = contactService.create(contact)
    # contactSchema = ContactMapper.fromModel(contact)
    # session.add(contactSchema)
    # session.commit()
    # session.refresh(contactSchema)
    # return contactSchema
    return contact


@app.get(
    "/contacts",
    tags=["Contacts"],
    summary="Get list of contacts",
    description="Returns the list of contacts",
    response_model=List[Contact]
)
def getContacts(skip: int = 0, limit: int = 100, session: Session = Depends(connector.getSession)):
    # contactSchemas = session.query(ContactSchema).offset(skip).limit(limit).all()
    # contacts = ContactMapper.fromSchemas(contactSchemas)
    contactService = ContactService()
    contacts = contactService.findByFilter(None)
    # contacts = contactService.findByFilter({"skip":skip, "limit":limit})

    return contacts


@app.get(
    "/contacts/{contact_id}",
    tags=["Contacts"],
    summary="Find Contact by ID",
    description="Returns the contact by ID",
    response_model=Contact
)
def getContact(contact_id: int, session: Session = Depends(connector.getSession)):
    # contactSchema = session.query(ContactSchema).filter(ContactSchema.id == contact_id).first()
    # if contactSchema is None:
    #     raise HTTPException(status_code=404, detail="Record not found!")
    #
    # contact = ContactMapper.fromSchema(contactSchema)

    contactService = ContactService()
    contacts = contactService.findByFilter({"id": contact_id})
    contact = contacts[0] if contacts else None
    return contact


if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=8082
    )
