#
# Author: Rohtash Lakra
#
import logging

from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from account.v1 import account_router
from framework.exception.auth import AuthenticationException
from framework.exception.duplicate import DuplicateRecordException
from framework.exception.not_found import NoRecordFoundException
from framework.exception.validation import ValidationException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import ErrorModel, ResponseModel
from rest.base import BaseRouter
from rest.user.model import LoginUser, User
from rest.user.service import UserService

logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="webapp/templates")
current_account = None


def _user_payload(user: User) -> dict:
    return user.model_dump(mode="json", exclude={"user_security", "addresses"})


@account_router.get("/register", include_in_schema=False)
async def register_view(request: Request):
    return templates.TemplateResponse("account/register.html", {"request": request})


@account_router.post("/register")
async def register(request: Request):
    payload = await BaseRouter.payload_or_none(request) or {}
    is_json_request = "application/json" in request.headers.get("content-type", "")
    user_data = {
        "user_name": payload.get("user_name"),
        "password": payload.get("password"),
        "first_name": payload.get("first_name"),
        "last_name": payload.get("last_name"),
        "email": payload.get("email"),
        "birth_date": payload.get("birth_date"),
    }
    try:
        user = User(**user_data)
        user_service = UserService()
        created_user = user_service.register(user)
        if is_json_request:
            return JSONResponse(status_code=201, content=_user_payload(created_user))
        return RedirectResponse(url="/accounts/login", status_code=303)
    except ValidationException as ex:
        if is_json_request:
            response = ErrorModel.buildError(HTTPStatus.INVALID_DATA, str(ex))
            return JSONResponse(status_code=response.status, content=response.model_dump(mode="json"))
        return RedirectResponse(url="/accounts/register", status_code=303)
    except DuplicateRecordException as ex:
        if is_json_request:
            response = ErrorModel.buildError(HTTPStatus.CONFLICT, str(ex))
            return JSONResponse(status_code=response.status, content=response.model_dump(mode="json"))
        return RedirectResponse(url="/accounts/register", status_code=303)


@account_router.get("/login", include_in_schema=False)
async def login_view(request: Request):
    return templates.TemplateResponse("account/login.html", {"request": request})


@account_router.post("/login")
async def login(request: Request):
    global current_account
    body = await BaseRouter.payload_or_none(request) or {}
    user_name = body.get("user_name") or body.get("email")
    is_json_request = "application/json" in request.headers.get("content-type", "")
    try:
        login_user = LoginUser(email=user_name, user_name=user_name, password=body.get("password"))
        user_service = UserService()
        user_service.login(login_user)
        users = user_service.findByFilter({"email": user_name})
        if not users:
            users = user_service.findByFilter({"user_name": user_name})
        if not users:
            raise NoRecordFoundException(HTTPStatus.NOT_FOUND, f"User '{user_name}' is not registered!")

        current_account = users[0]
        if is_json_request:
            return JSONResponse(status_code=200, content=_user_payload(current_account))
        return RedirectResponse(url="/accounts/profile", status_code=303)
    except NoRecordFoundException as ex:
        if is_json_request:
            response = ErrorModel.buildError(HTTPStatus.NOT_FOUND, str(ex))
            return JSONResponse(status_code=response.status, content=response.model_dump(mode="json"))
        return RedirectResponse(url="/accounts/login", status_code=303)
    except AuthenticationException as ex:
        if is_json_request:
            response = ErrorModel.buildError(HTTPStatus.UNAUTHORIZED, str(ex))
            return JSONResponse(status_code=response.status, content=response.model_dump(mode="json"))
        return RedirectResponse(url="/accounts/login", status_code=303)


@account_router.get("/profile", include_in_schema=False)
async def profile_view(request: Request):
    context = {
        "request": request,
        "account": current_account,
    }
    return templates.TemplateResponse("account/profile.html", context)


@account_router.post("/profile", include_in_schema=False)
async def profile_update(request: Request):
    global current_account
    form = await request.form()
    try:
        user_service = UserService()
        target_account = current_account
        submitted_user_name = form.get("user_name")
        submitted_email = form.get("email")
        submitted_id = form.get("id")

        if target_account is None:
            if submitted_id:
                users = user_service.findByFilter({"id": int(submitted_id)})
            elif submitted_email:
                users = user_service.findByFilter({"email": submitted_email})
            elif submitted_user_name:
                users = user_service.findByFilter({"user_name": submitted_user_name})
            else:
                users = []
            if not users:
                return RedirectResponse(url="/accounts/login", status_code=303)
            target_account = users[0]

        updated_user = User(
            id=target_account.id,
            user_name=submitted_user_name,
            first_name=form.get("first_name"),
            last_name=form.get("last_name"),
            email=submitted_email,
            birth_date=form.get("birth_date"),
            admin=target_account.admin,
            last_seen=target_account.last_seen,
            avatar_url=target_account.avatar_url,
            password=target_account.password,
        )
        current_account = user_service.update(updated_user)
    except Exception as ex:
        logger.exception("profile_update failed")
    return RedirectResponse(url="/accounts/profile", status_code=303)


@account_router.get("/forgot-password", include_in_schema=False)
async def forgot_password(request: Request):
    return templates.TemplateResponse("account/forgot-password.html", {"request": request})


@account_router.post("/logout")
async def logout():
    return JSONResponse(status_code=200, content=ResponseModel.jsonResponse(HTTPStatus.OK, message="Logged out"))


@account_router.get("/notifications", include_in_schema=False)
async def notifications(request: Request):
    return templates.TemplateResponse("account/notifications.html", {"request": request})
