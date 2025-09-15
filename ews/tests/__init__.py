#
# Author: Rohtash Lakra
#
from webapp import create_app

# setup webapp for testing
app = create_app()
# app.app_context = app.app_context()
app_context = app.app_context()
# app.app_context.push()
app_context.push()
