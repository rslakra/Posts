#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-project/
#
from webapp import WebApp

webApp = WebApp()
app = webApp.create_app()

# App Main
# If you do need to have executable code within your 'routes.py' file, enclose it in the "if __name__ == '__main__':"
# block. This ensures the code only runs when the file is executed directly, not when imported.
if __name__ == "__main__":
    """
    Main Application

    How to run:
    - python3 webapp.py
    - python -m flask --app webapp run --port 8080 --debug
    """
    # create an app
    webApp.run()
