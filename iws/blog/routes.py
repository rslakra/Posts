#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-blueprint/
#
import json

from flask import current_app, render_template, make_response, request, redirect
from blog.v1 import bp as bp_v1_blogs
import time
import logging

logger = logging.getLogger(__name__)


@bp_v1_blogs.get("/")
def index():
    """Load Index Page"""
    logger.info(f"index={request}")
    posts = [
        {
            "title": "Are blogs important for businesses?",
            "description": "Blogs are an important part of a company’s content strategy, as they can communicate the features and benefits of a product or service.",
            "author": "Rohtash",
            "posted_on": "2024-10-13T00:20:27.466337"
        },
        {
            "title": "How should you format a blog post?",
            "description": "A blog post should be formatted in a way that leads to increased readership and interest. Beginning with an attention-grabbing headline, a well-formatted blog post should also feature relatively brief sentences that convey ideas quickly. The post should also include subheads or section heads, helping readers to quickly understand the message or skip to sections that are more interesting to them. Additionally, photos and other graphics can increase readership, interest, and SEO rankings across search engines.",
            "author": "R. Lakra",
            "posted_on": "2024-10-23T00:40:21.466337"
        }
    ]

    context = {
        'strftime': time.strftime
    }

    current_app.logger.debug(f"posts={json.dumps(posts)}")
    return render_template("blog/index.html", posts=posts, **context)


@bp_v1_blogs.route('/create', methods=['GET', 'POST'])
def create():
    """Load Create/Add Post Page"""
    logger.info(f"index={request}")
    if request.method == 'POST':
        body = request.get_json()
        print(f"body={body}")
        return redirect('/')

    """Render Add Post Page"""
    return render_template("blog/create.html")
