#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-blueprint/
#
from flask import render_template, make_response, request, redirect, url_for, current_app

from account.entity import User
from account.v1 import bp as bp_v1_accounts
from framework.http import HTTPStatus
from framework.orm.pydantic.model import ErrorModel, ResponseModel
from rest.user.model import User

# holds accounts in memory

accounts = []


# Returns the next ID of the user
def _find_next_id():
    last_id = 0
    if not accounts and len(accounts) > 0:
        last_id = max(account["id"] for account in accounts)

    return last_id + 1


# register a new user
# @bp.route("/register", methods=[HTTPMethod.GET, HTTPMethod.POST])
@bp_v1_accounts.get("/register")
def register_view():
    """
    register a new user
    """
    current_app.logger.debug(f"register_view => {request}")
    return render_template("account/register.html")


@bp_v1_accounts.post("/register")
def register():
    current_app.logger.debug(f"register => {request}")
    user = None
    response_json = None
    if request.is_json:
        body = request.get_json()
        user = User.from_json(body)
        # user = User(**body)
        user.id = _find_next_id()
        accounts.append(user)
        # response_json = ResponseEntity.build_response_json(HTTPStatus.CREATED, user)
        response_json = user.json()
    else:
        response_json = ResponseModel.jsonResponse(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, instance=user,
                                                   message="Invalid JSON object!")

    return make_response(response_json)


# login to an user
@bp_v1_accounts.get("/login")
def login_view():
    """
    login to an user
    """
    current_app.logger.debug(f"login_view => {request}")
    return render_template("account/login.html")


@bp_v1_accounts.post("/login")
# @bp_v1_accounts.route('/login', methods=['POST'])
def login():
    current_app.logger.debug(f"login => {request}")
    print(request)
    if request.is_json:
        user = request.get_json()
        current_app.logger.debug(f"user{user}")
        if not accounts:
            for account in accounts:
                if account['user_name'] == user.user_name:
                    return make_response(HTTPStatus.OK, account)
    else:
        user = None
        # user = get_user(request.form['username'])
        if user and user.check_password(request.form['password']):
            # login_user(user)
            current_app.logger.info('%s logged in successfully', user.username)
            return redirect(url_for('index'))
        else:
            current_app.logger.info('%s failed to log in', user.username)
            # abort(401)

    response = ErrorModel.jsonResponse(HTTPStatus.NOT_FOUND, "Account is not registered!")
    # response = ErrorModel.buildError(HTTPStatus.NOT_FOUND, "Account is not registered!")
    current_app.logger.debug(f"response{response}")
    return make_response(response)


# view profile
@bp_v1_accounts.get("/profile")
def profile_view():
    """
    view profile
    """
    return render_template("account/profile.html")


# forgot-password
@bp_v1_accounts.get("/forgot-password")
def forgot_password():
    """
    forgot-password
    """
    return render_template("account/forgot-password.html")


# Logout Page
@bp_v1_accounts.post("/logout")
def logout():
    """
    About Us Page
    """
    # return render_template("index.html")
    return redirect(url_for('iws.webapp.index'))


# accounts home page
@bp_v1_accounts.get("/notifications")
def notifications():
    """
    Services Page
    """
    return render_template("account/notifications.html")
