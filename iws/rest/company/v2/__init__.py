#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-blueprint/
#
from flask import Blueprint

bp = Blueprint("companies", __name__, url_prefix="/companies")
"""
Making a Flask Blueprint:

Create an instance of Blueprint prefixed with '/bp' as named bp.
Parameters:
    name: represents the name of the blueprint, which Flask’s routing mechanism uses and identifies it in the project.
    __name__: The Blueprint’s import name, which Flask uses to locate the Blueprint’s resources.
    url_prefix: the path to prepend to all of the Blueprint’s URLs.

There are other optional arguments that you can provide to alter the Blueprint’s behavior:

static_folder: the folder where the Blueprint’s static files can be found
static_url_path: the URL to serve static files from
template_folder: the folder containing the Blueprint’s templates
url_prefix: the path to prepend to all of the Blueprint’s URLs
subdomain: the subdomain that this Blueprint’s routes will match on by default
url_defaults: a dictionary of default values that this Blueprint’s views will receive
root_path: the Blueprint’s root directory path, whose default value is obtained from the Blueprint’s import name

Note that all paths, except root_path, are relative to the Blueprint’s directory.

However, a Flask Blueprint is not actually an application. It needs to be registered in an application before you can run it. 
When you register a Flask Blueprint in an application, you’re actually extending the application with the contents of the Blueprint.
This is the key concept behind any Flask Blueprint. They record operations to be executed later when you register them on an application.

The Blueprint object 'bp' has methods and decorators that allow you to record operations to be executed when registering 
the Flask Blueprint in an application to extend it.

Here are the Blueprint objects most used decorators that you may find useful:

- '.route()' to associate a view function to a URL route
- '.errorhandler()' to register an error handler function
- '.before_request()' to execute an action before every request
- '.after_request()' to execute an action after every request
- '.app_template_filter()' to register a template filter at the application level

When you register the Flask Blueprint in an application, you extend the application with its contents.

"""
from rest.company import routes
from rest.company.v2.routes import *
