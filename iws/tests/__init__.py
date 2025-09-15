#
# Author: Rohtash Lakra
#
from webapp import WebApp

# setup webapp for testing
webApp = WebApp()
app = webApp.create_app(test_mode=True)
# app.app_context = app.app_context()
app_context = app.app_context()
# app.app_context.push()
app_context.push()

#
# app.app_context = app.app_context()
# app.app_context.push()