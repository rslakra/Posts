#
# Author: Rohtash Lakra
#
import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from admin.v1 import admin_router
from framework.http import HTTPStatus
from framework.orm.pydantic.model import ErrorModel

logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="webapp/templates")
accounts = []


def _find_next_id():
    return (max((account.get("id", 0) for account in accounts), default=0) + 1)


@admin_router.get("/", include_in_schema=False)
async def index(request: Request):
    return templates.TemplateResponse("admin/index.html", {"request": request})


@admin_router.get("/register", include_in_schema=False)
async def register(request: Request):
    return templates.TemplateResponse("admin/register.html", {"request": request})


@admin_router.post("/register")
async def post_register(request: Request):
    user = await request.json()
    user["id"] = _find_next_id()
    accounts.append(user)
    return JSONResponse(status_code=201, content=user)


@admin_router.get("/login", include_in_schema=False)
async def login(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})


@admin_router.post("/login")
async def post_login(request: Request):
    user = await request.json()
    for account in accounts:
        if account.get("user_name") == user.get("user_name"):
            return JSONResponse(status_code=200, content=account)

    response = ErrorModel.buildError(HTTPStatus.NOT_FOUND, "Account is not registered!")
    return JSONResponse(status_code=response.status, content=response.model_dump(mode="json"))


@admin_router.get("/profile", include_in_schema=False)
async def profile(request: Request):
    return templates.TemplateResponse("admin/profile.html", {"request": request})


@admin_router.get("/forgot-password", include_in_schema=False)
async def forgot_password(request: Request):
    return templates.TemplateResponse("admin/forgot-password.html", {"request": request})


@admin_router.post("/logout")
async def logout():
    return JSONResponse(status_code=200, content={"message": "Logged out"})
