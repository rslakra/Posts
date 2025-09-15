#
# Author: Rohtash Lakra
#
# from logger.logutils import RequestIdFilter
#
# reqeustIdFilter = RequestIdFilter()
# https://dev.to/camillehe1992/mask-sensitive-data-using-python-built-in-logging-module-45fa

import json
import logging
import re
from copy import deepcopy
from sys import stdout

import requests
from flask import Flask, g, has_request_context, request
from flask.logging import default_handler
from flask_log_request_id import RequestID, RequestIDLogFilter

from framework.enums import EnvType, KeyEnum

UTF_8 = 'utf-8'
LOG_LEVEL = logging.DEBUG
DEFAULT_LOG_FORMAT = "[%(asctime)s] [%(process)d] [%(levelname)s] - %(message)s"
REQUEST_ID_LOG_FORMAT = "[%(asctime)s] [%(process)d] [%(levelname)s] [%(request_id)s] - %(message)s"
DETAILED_LOG_FORMAT = "[%(asctime)s] [%(process)d] [%(levelname)s] [%(filename)s:%(lineno)s] - %(message)s"

DATE_FORMAT_TZ = "%Y-%m-%d %H:%M:%S %z"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT_MSEC = "%Y-%m-%d %H:%M:%S.%f,%03d"

# Configure app default loggers
logging.basicConfig(level=LOG_LEVEL, format=DETAILED_LOG_FORMAT, force=True)
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
# datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f %z")[:23]
# logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)


# init logger
logger = logging.getLogger(__name__)

# 1. Define the regex patterns of sensitive data
sensitive_regex_patterns = [
    # U.S. Social Security numbers
    r"\d{3}-\d{2}-\d{4}",
    # Credit card numbers
    r"\d{4}-\d{4}-\d{4}-\d{4}",
]

# 2. Define a list of keys that values are sensitive data
sensitive_keys = (
    "headers",
    "credentials",
    "Authorization",
    "token",
    "password",
    "phone_number",
    "email"
)


class SensitiveDataFilter(logging.Filter):
    sensitive_regex_patterns = sensitive_regex_patterns
    sensitive_keys = sensitive_keys

    def filter(self, record):
        try:
            record.args = self.mask_sensitive_args(record.args)
            record.msg = self.mask_sensitive_data(record.msg)
            return True
        except Exception as ex:
            logger.error(f"Error={ex}")
            return True

    def mask_sensitive_args(self, args):
        if isinstance(args, dict):
            masked_args = args.copy()
            for key in args.keys():
                if key in sensitive_keys:
                    masked_args[key] = "******"
                else:
                    # mask sensitive data in dict values
                    masked_args[key] = self.mask_sensitive_data(args[key])

            return masked_args

        # when there are multi arg in record.args
        return tuple([self.mask_sensitive_data(arg) for arg in args])

    def mask_sensitive_data(self, message):
        # mask sensitive data in multi record.args
        if isinstance(message, dict):
            return self.mask_sensitive_args(message)

        # mask sensitive data in message
        if isinstance(message, str):
            for pattern in self.sensitive_regex_patterns:
                message = re.sub(pattern, "******", message)

            # replace sensitive data with asterisks
            for key in self.sensitive_keys:
                pattern_str = rf"'{key}': '[^']+'"
                replace = f"'{key}': '******'"
                message = re.sub(pattern_str, replace, message)

        return message


class DefaultLogger(logging.LoggerAdapter):
    """Default logger for an application that handles displaying debugging data for critical errors, when 'extra' arg
    is passed and contains 'debug_data' in dict.
    """

    def __init__(self, app=None, level: int = LOG_LEVEL, extra={}):
        self.app = app
        app.logger.setLevel(level)
        super().__init__(app.logger, extra)
        # Setup default logging
        # https://pypi.org/project/Flask-3-Log-Request-ID/
        RequestID(app)

        # Adding also the gunicorn handlers to the app.logger
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.debug(f"app.logger.handlers={app.logger.handlers}")
        app.logger.debug(f"gunicorn_logger.handlers={gunicorn_logger.handlers}")
        app.logger.handlers = gunicorn_logger.handlers
        # for handler in gunicorn_logger.handlers:
        #     app.logger.info(f"handler={handler}")
        #     app.logger.addHandler(handler)

        # keep lower logger level
        app.logger.debug(f"app.logger.level={app.logger.level}, gunicorn_logger.level={gunicorn_logger.level}")
        if app.logger.getEffectiveLevel() < gunicorn_logger.level:
            app.logger.info(f"Using gunicorn_logger.level={gunicorn_logger.level}")
            app.logger.setLevel(gunicorn_logger.level)

        # Use custom loggers instead
        app.logger.debug(f"default_handler={default_handler}")
        app.logger.removeHandler(default_handler)

        # update log handlers with customer json formatter
        for handler in app.logger.handlers:
            # all log formatter and request-id filter
            handler.setFormatter(LogJSONFormatter(fmt=DETAILED_LOG_FORMAT))
            handler.addFilter(RequestIDLogFilter())
            handler.addFilter(SensitiveDataFilter())

    def logConfig(self):
        logger.debug("logConfig()")
        # logger = self.app.logger
        # register logger here root logger
        if EnvType.is_production(EnvType.get_env_type()):
            logFileName = self.app.get_env(KeyEnum.LOG_FILE_NAME.name)
            logFileHandler = logging.FileHandler(logFileName)
            logger.debug(f"logFileName={logFileName}, logFileHandler=[{logFileHandler}]")
            # set format and filters
            logFileHandler.setFormatter(LogJSONFormatter(fmt=DETAILED_LOG_FORMAT))
            logFileHandler.addFilter(RequestIDLogFilter())
            logFileHandler.addFilter(SensitiveDataFilter())
            # logging.getLogger().addHandler(logFileHandler)
            logging.basicConfig(filename=logFileName, encoding=UTF_8, level=LOG_LEVEL, format=DETAILED_LOG_FORMAT)
            requests.packages.urllib3.add_stderr_logger()

    def process(self, msg, kwargs):
        extra = kwargs.get('extra', {})
        debug_data = extra.get('debug_data', {})
        if debug_data:
            msg = f"{msg} | Debug Data: {debug_data}"

        return msg, kwargs


def mask_data(data: dict):
    """
    Recursively masks Personally Identifiable Information (PII) like phone numbers and emails in logs.
    Arguments:
        data (dict): The dictionary containing data to be masked.

    Returns:
        dict: The dictionary with PII masked, where applicable.
    """

    if not isinstance(data, dict):
        return data

    # Define keys that represent PII data
    mask_fields = ['phone_number', 'email']
    for key, val in data.items():
        # Check if the key is a PII key
        if key in mask_fields and isinstance(val, str):
            # Mask the value (e.g., replace with asterisks)
            data[key] = '*' * len(val)
        # If the value is a dictionary, call the function recursively
        elif isinstance(val, dict):
            data[key] = mask_data(val)
        # If the value is a list, iterate and check each element
        elif isinstance(val, list):
            data[key] = [mask_data(item) if isinstance(item, dict) else item for item in val]

    return data


class LogJSONFormatter(logging.Formatter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def formatMessage(self, record):
        """
        Formats the log record into a JSON structure with extra information like
        request details, user ID, session ID, and platform. Also masks PII data if applicable.

        Args:
            record (logging.LogRecord): The log record to format
                - `message` (str): The main log message.
                - `extra_info` (dict, optional): Additional data passed to the logger, typically in the form of
                    a dictionary

        Returns:
            str: A formatted log message in JSON format, or a fallback message in case of errors

        Example:
            ```python
            logger.info(
                "User info",
                extra={ 'extra_info': { 'email': 'user@example.com', 'phone_number': '1234567890' }}
            )
            ```
        """
        message = record.getMessage()

        # skipping logger formatting for testing
        if EnvType.is_testing(EnvType.get_env_type()):
            return message

        log_message = f'[{self.formatTime(record, DATE_FORMAT_MSEC)}] [{record.process}] [{record.levelname}]'

        if has_request_context() and hasattr(g, 'log_request_id'):
            log_message += f' [{g.log_request_id}]'

        try:
            if hasattr(record, 'extra_info'):
                log_record = {
                    'message': message,
                    'endpoint': request.full_path if request else None,
                }
                # Must use try/except otherwise tests fail
                try:
                    # Attempt to capture request payload
                    log_record['request_payload'] = request.get_json() if request.is_json else request.get_data(
                        as_text=True)
                except Exception as ex:
                    logger.error(f"Log formatting error={ex}")
                    # Fallback if the request body can't be accessed
                    log_record['request_payload'] = None

                # If a request context is active, capture user and session info
                if has_request_context():
                    if request:
                        log_record['headers'] = {k: v for k, v in dict(request.headers).items() if
                                                 not k.startswith("Cloudfront")}
                    # Add request-related data
                    log_record.update({
                        'user_id': g.user_security.get('user_id') if hasattr(g, 'user_security') else None,
                        'session_id': g.get('user_session_id'),
                        'platform': g.user_agent.get('platform') if hasattr(g, 'user_agent') else None
                    })

                if isinstance(record.extra_info, dict) and record.extra_info:
                    # only if the user_id is present in the log_record will personal information be masked
                    if log_record['user_id']:
                        update_data = mask_data(deepcopy(record.extra_info))
                    else:
                        update_data = record.extra_info
                    log_record.update(update_data)
                else:
                    log_record['data'] = record.extra_info

                message = json.dumps(log_record, default=str, indent=2)

        except Exception as e:
            # Log formatting errors as a fallback
            message = f"Error formatting log: {e}"

        return log_message + f' - {message}'


class ColoredLogFactory:
    """Custom color logger."""

    def formatter(log: dict) -> str:
        """
        Format log colors based on level.

        :param dict log: Logged event stored as map containing contextual metadata.

        :returns: str
        """
        if log["level"].name == "INFO":
            return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #b3cfe7>{level}</fg #b3cfe7>: <light-white>{message}</light-white>\n"
        if log["level"].name == "WARNING":
            return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #b09057>{level}</fg #b09057>: <light-white>{message}</light-white>\n"
        if log["level"].name == "SUCCESS":
            return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #6dac77>{level}</fg #6dac77>: <light-white>{message}</light-white>\n"
        if log["level"].name == "ERROR":
            return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #a35252>{level}</fg #a35252>: <light-white>{message}</light-white>\n"

        return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #b3cfe7>{level}</fg #b3cfe7>: <light-white>{message}</light-white>\n"

    def get_logger(self):
        """Create custom logger."""
        self.remove()
        self.add(stdout, colorize=True, format=self.formatter())

        return self


# logFactory = ColoredLogFactory()
# LOGGER = logFactory.get_logger()
