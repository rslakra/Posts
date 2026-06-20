#
# Author: Rohtash Lakra
#
import logging
import time

from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from blog.v1 import blog_router

logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="webapp/templates")


@blog_router.get("/", include_in_schema=False)
async def index(request: Request):
    posts = [
        {"title": "Are blogs important for businesses?", "description": "Blogs are an important part of a company’s content strategy, as they can communicate the features and benefits of a product or service.", "author": "Rohtash", "posted_on": "2024-10-13T00:20:27.466337"},
        {"title": "How should you format a blog post?", "description": "A blog post should be formatted in a way that leads to increased readership and interest.", "author": "R. Lakra", "posted_on": "2024-10-23T00:40:21.466337"},
    ]
    context = {"request": request, "posts": posts, "strftime": time.strftime}
    return templates.TemplateResponse("blog/index.html", context)


@blog_router.get("/create", include_in_schema=False)
async def create_get(request: Request):
    return templates.TemplateResponse("blog/create.html", {"request": request})


@blog_router.post("/create")
async def create_post(request: Request):
    await request.json()
    return RedirectResponse(url="/blogs/", status_code=303)
