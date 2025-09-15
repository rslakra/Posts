#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-blueprint/
#
from flask import render_template, make_response, request, redirect, url_for

from admin.v1 import bp as bp_v1_admin
from framework.http import HTTPStatus
from framework.orm.pydantic.model import ErrorModel

# holds accounts in memory
accounts = []


# Returns the next ID of the user
def _find_next_id():
    last_id = 0
    if not accounts and len(accounts) > 0:
        last_id = max(account["id"] for account in accounts)

    return last_id + 1


# register a new user
@bp_v1_admin.route("/")
def index():
    """
    register a new user
    """
    return render_template("admin/index.html")


# register a new user
@bp_v1_admin.get("/register")
def register():
    """
    register a new user
    """
    return render_template("admin/register.html")


@bp_v1_admin.post("/register")
def post_register():
    print(request)
    if request.is_json:
        user = request.get_json()
        user["id"] = _find_next_id()
        accounts.append(user)
        return user, 201

    return make_response(ErrorModel(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "Invalid JSON object!"))


# login to an user
@bp_v1_admin.get("/login")
def login():
    """
    login to an user
    """
    return render_template("admin/login.html")


@bp_v1_admin.post("/login")
def post_login():
    print(request)
    if request.is_json:
        user = request.get_json()
        print(f"user:{user}")
        if not accounts:
            for account in accounts:
                if account['user_name'] == user.user_name:
                    return make_response(HTTPStatus.OK, account)

    response = ErrorModel.get_error(HTTPStatus.NOT_FOUND, "Account is not registered!")
    print(response)

    return make_response(response)


# view profile
@bp_v1_admin.get("/profile")
def profile():
    """
    view profile
    """
    return render_template("admin/profile.html")


# forgot-password
@bp_v1_admin.get("/forgot-password")
def forgot_password():
    """
    forgot-password
    """
    return render_template("admin/forgot-password.html")


# Logout Page
@bp_v1_admin.post("/logout")
def logout():
    """
    About Us Page
    """
    # return render_template("index.html")
    return redirect(url_for('iws.webapp.index'))
