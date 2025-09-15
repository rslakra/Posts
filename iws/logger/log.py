#
# Author: Rohtash Lakra
# References:
#  - https://blog.mcpolemic.com/2016/01/18/adding-request-ids-to-flask.html
#  - https://docs.python.org/3/howto/logging-cookbook.html#adding-contextual-information-to-your-logging-output
#  - https://esgi-dendyanri.medium.com/python-flask-logging-with-id-on-each-request-aad7c45c1f8e
#
# But I wonder if defining @app.before_request and putting a request ID there wouldn't be a better idea?
#
# formatter = logging.Formatter('[%(asctime)s] - [%(threadName)s] [%(thread)d] - %(levelname)s in %(module)s at %(lineno)d: %(message)s')
# Default:
# "format": "%(asctime)s - %(levelname)s - %(request_id)s - %(name)s.%(module)s.%(funcName)s:%(lineno)d - %(message)s"
# "format": "[%(asctime)s] - [%(threadName)s] [%(thread)d] - %(levelname)s in %(module)s at %(lineno)d: %(message)s"
# "format": "[%(asctime)s] - %(levelname)s - (%(request_id)s) - %(name)s.%(module)s.%(funcName)s:%(lineno)d - %(message)s"

import logging.config

# log-config
LOG_CONFIG = {
    "version": 1,
    "filters": {
        "request_id": {
            "()": "logutils.RequestIdFilter"
        }
    },
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] - [%(levelname)-8s] - (%(request_id)s) - %(name)s.%(module)s.%(funcName)s:%(lineno)d - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "filters": [
                "request_id"
            ],
            "formatter": "standard"
        }
    },
    "loggers": {
        "": {
            "handlers": [
                "console"
            ],
            "level": "DEBUG"
        },
        "app": {
            "handlers": [
                "console"
            ],
            "level": "DEBUG"
        }
    }
}

# set up our logging format
logging.config.dictConfig(LOG_CONFIG)
