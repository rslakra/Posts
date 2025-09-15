#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-project/
#
import os
from webapp import create_app

# init app by calling crate api function.
app = create_app()

"""
Run Web Application

Configure the app here.
"""


def run_web_app():
    # localhost
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 8080))
    debug = bool(os.getenv("DEBUG_ENABLED", True))

    # run application with params
    app.run(host=host, port=port, debug=debug)


"""
Main Application

How to run:
- python3 webapp.py
- python -m flask --app webapp run --port 8080 --debug

"""
# App Main
# If you do need to have executable code within your 'routes.py' file, enclose it in the "if __name__ == '__main__':"
# block. This ensures the code only runs when the file is executed directly, not when imported.
if __name__ == "__main__":
    run_web_app()
