#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-blueprint/
#
from flask import render_template, make_response, request, redirect, url_for
from comment.v1 import bp as bp_v1_comments


@bp_v1_comments.route("/")
def index():
    """Load Index Page"""
    return render_template("comment/index.html")


@bp_v1_comments.get("/comment/<int:comment_id>")
def login():
    """Load View Page"""
    return render_template("comment/view.html")


@bp_v1_comments.get("/checkout")
def checkout():
    """Load Checkout Page"""
    return render_template("comment/checkout.html")
