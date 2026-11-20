#
# Author: Rohtash Lakra
#
import logging

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

from account.v1 import account_router
from admin.v1 import admin_router
from blog.v1 import blog_router
from comment.v1 import comment_router
from framework.exception.duplicate import DuplicateRecordException
from framework.exception.validation import ValidationException
from framework.http import HTTPStatus
from post.v1 import post_router
from rest.contact.model import Contact
from rest.contact.service import ContactService
from framework.orm.sqlalchemy.schema import SchemaOperation

logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="webapp/templates")

# Named router for webapp UI routes.
webapp_router = APIRouter()


# Public UI landing page.
@webapp_router.get("/", include_in_schema=False)
async def index(request: Request):
    logger.debug(f"index={request.url.path}")
    return templates.TemplateResponse("index.html", {"request": request})


@webapp_router.get("/about-us", include_in_schema=False)
async def about(request: Request):
    logger.debug(f"about={request.url.path}")
    return templates.TemplateResponse("about.html", {"request": request})


@webapp_router.get("/services", include_in_schema=False)
async def services(request: Request):
    logger.debug(f"services={request.url.path}")
    return templates.TemplateResponse("services.html", {"request": request})


@webapp_router.get("/clients", include_in_schema=False)
async def clients(request: Request):
    logger.debug(f"clients={request.url.path}")
    return templates.TemplateResponse("clients.html", {"request": request})


@webapp_router.api_route("/contact-us", methods=["GET", "POST"], include_in_schema=False)
async def contact(request: Request):
    if request.method == "GET":
        return templates.TemplateResponse("contact.html", {"request": request})

    # POST: parse form and map to Contact domain model.
    form = await request.form()
    payload = {
        "first_name": form.get("first_name"),
        "last_name": form.get("last_name"),
        "country": form.get("country"),
        "subject": form.get("subject"),
    }
    logger.info(f"contact payload_keys={list(payload.keys())} country={payload.get('country')}")

    try:
        # Validate + persist using existing contact service layer used by APIs.
        contact_model = Contact(**payload)
        contact_service = ContactService()
        contact_service.validate(SchemaOperation.CREATE, contact_model)
        contact_service.create(contact_model)
        logger.info("contact submit created successfully")
        return templates.TemplateResponse(
            "contact.html",
            {"request": request, "success_message": "Contact submitted successfully."}
        )
    except ValidationException as ex:
        # Keep validation feedback on same page for better UX.
        logger.warning(f"contact submit validation error={ex}")
        return templates.TemplateResponse(
            "contact.html",
            {"request": request, "error_message": "Please fill all required contact fields."},
            status_code=HTTPStatus.INVALID_DATA.statusCode
        )
    except DuplicateRecordException as ex:
        # Surface uniqueness conflict as user-facing message.
        logger.warning(f"contact submit duplicate error={ex}")
        return templates.TemplateResponse(
            "contact.html",
            {"request": request, "error_message": "A contact with this subject already exists."},
            status_code=HTTPStatus.CONFLICT.statusCode
        )
    except Exception as ex:
        # Catch-all prevents UI crash and keeps actionable logs.
        logger.exception("contact submit unexpected error")
        return templates.TemplateResponse(
            "contact.html",
            {"request": request, "error_message": "Unable to submit contact right now."},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.statusCode
        )


@webapp_router.get("/logout", include_in_schema=False)
async def logout(request: Request):
    logger.debug(f"logout={request.url.path}")
    return templates.TemplateResponse("logout.html", {"request": request})


@webapp_router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("webapp/static/images/webapp-logo.png")


# Compose feature routers under webapp for UI + feature endpoints.
webapp_router.include_router(account_router)
webapp_router.include_router(admin_router)
webapp_router.include_router(blog_router)
webapp_router.include_router(comment_router)
webapp_router.include_router(post_router)
