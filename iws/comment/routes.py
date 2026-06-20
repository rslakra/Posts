#
# Author: Rohtash Lakra
#
from fastapi import Request
from fastapi.templating import Jinja2Templates

from comment.v1 import comment_router

templates = Jinja2Templates(directory="webapp/templates")


@comment_router.get("/", include_in_schema=False)
async def index(request: Request):
    return templates.TemplateResponse("comment/index.html", {"request": request})


@comment_router.get("/comment/{comment_id}", include_in_schema=False)
async def view(request: Request, comment_id: int):
    return templates.TemplateResponse("comment/view.html", {"request": request, "comment_id": comment_id})


@comment_router.get("/checkout", include_in_schema=False)
async def checkout(request: Request):
    return templates.TemplateResponse("comment/checkout.html", {"request": request})
