#
# Author: Rohtash Lakra
#
import json
import time

from fastapi import Request, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from post.v1 import post_router

templates = Jinja2Templates(directory="webapp/templates")


@post_router.get("/", include_in_schema=False)
async def index(request: Request):
    posts = [
        {"title": "Are blogs important for businesses?", "description": "Blogs are an important part of a company’s content strategy, as they can communicate the features and benefits of a product or service.", "author": "Rohtash", "posted_on": "2024-10-13T00:20:27.466337"},
        {"title": "How should you format a blog post?", "description": "A blog post should be formatted in a way that leads to increased readership and interest.", "author": "R. Lakra", "posted_on": "2024-10-23T00:40:21.466337"},
    ]
    # Keep template context explicit so Jinja does not fail on optional sections.
    return templates.TemplateResponse(
        "post/index.html",
        {"request": request, "posts": posts, "files": [], "strftime": time.strftime, "posts_json": json.dumps(posts)}
    )


@post_router.get("/create", include_in_schema=False)
async def create_get(request: Request):
    return templates.TemplateResponse("post/create.html", {"request": request})


@post_router.post("/create")
async def create_post(request: Request):
    await request.json()
    return RedirectResponse(url="/posts/", status_code=303)


@post_router.get("/upload", include_in_schema=False)
async def upload_get(request: Request):
    return templates.TemplateResponse("post/upload_file.html", {"request": request})


@post_router.post("/upload", include_in_schema=False)
async def upload_post(request: Request, file: UploadFile = File(...)):
    upload_metadata = {"message": f"Uploaded: {file.filename}"}
    return templates.TemplateResponse(
        "post/index.html",
        {"request": request, "upload_metadata": upload_metadata, "posts": [], "files": []}
    )
