#
# Author: Rohtash Lakra
#
from functools import lru_cache
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from globals import connector
from rest.contact.model import Contact
from rest.contact.service import ContactService
from settings import ConfigSetting

api_router = APIRouter()


@lru_cache
def getSettings():
    return ConfigSetting()


@api_router.get("/api/common/health", tags=["Common API Endpoints"], include_in_schema=False)
async def health():
    return JSONResponse(status_code=200, content={"message": "ok"})


@api_router.get("/health-check", tags=["Default Resources"], summary="Health Check", description="Returns Health Check Status")
async def healthCheck() -> JSONResponse:
    """The Health Check endpoint.
    Returns a default success message indicating the application is running.
    """
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "FastAPI ./v2/health-check"})


@api_router.get("/info", tags=["Default Resources"], summary="Get Configs", description="Get '.env' Configs")
async def info(config: ConfigSetting = Depends(getSettings)):
    return config.model_dump()


@api_router.post(
    "/contacts",
    tags=["Contacts"],
    summary="Create Contact",
    description="Creates a new contact",
    response_model=Contact
)
def createContact(contact: Contact, session: Session = Depends(connector.getSession)):
    contactService = ContactService()
    contact = contactService.create(contact)
    return contact


@api_router.get(
    "/contacts",
    tags=["Contacts"],
    summary="Get list of contacts",
    description="Returns the list of contacts",
    response_model=List[Contact]
)
def getContacts(skip: int = 0, limit: int = 100, session: Session = Depends(connector.getSession)):
    contactService = ContactService()
    contacts = contactService.findByFilter(None)
    return contacts


@api_router.get(
    "/contacts/{contact_id}",
    tags=["Contacts"],
    summary="Find Contact by ID",
    description="Returns the contact by ID",
    response_model=Contact
)
def getContact(contact_id: int, session: Session = Depends(connector.getSession)):
    contactService = ContactService()
    contacts = contactService.findByFilter({"id": contact_id})
    contact = contacts[0] if contacts else None
    return contact
