#
# Author: Rohtash Lakra
#
import logging
import os
import re
import sys
import traceback
import uuid

import requests

from framework.enums import BaseEnum
from framework.time import StopWatch

# logger
logger = logging.getLogger(__name__)

# Upper-case letters
CAPITALS = re.compile('([A-Z])')


class Utils(BaseEnum):

    @staticmethod
    def randomUUID() -> str:
        """Generate a random UUID (Universally Unique Identifier)."""
        return uuid.uuid4().hex

    @staticmethod
    def stackTrace(exception: Exception):
        """Returns the string representation of exception"""
        exc_info = sys.exc_info()
        return ''.join(traceback.format_exception(*exc_info))

    @staticmethod
    def exception(exception: Exception, message: str):
        return exception(message)

    @staticmethod
    def camelCaseToSnakeCase(text):
        """Convert a camel cased text to PEP8 style."""
        converted = CAPITALS.sub(lambda m: '_' + m.groups()[0].lower(), text)
        if converted[0] == '_':
            return converted[1:]
        else:
            return converted

    @staticmethod
    def snakeCaseToCamelCase(text, initial=False):
        """Convert a PEP8 style text to camel case."""
        chunks = text.split('_')
        converted = [s[0].upper() + s[1:].lower() for s in chunks]
        if initial:
            return ''.join(converted)
        else:
            return chunks[0].lower() + ''.join(converted[1:])

    @staticmethod
    def abs_path(file_name) -> str:
        """Returns the absolute path of the given file."""
        return os.path.abspath(os.path.dirname(file_name))

    @staticmethod
    def exists(path) -> bool:
        """Returns true if the path exists otherwise false."""
        return os.path.exists(path)

    @staticmethod
    def measure_ttfb(url):
        logger.debug(f"+measure_ttfb({url})")
        _watcher = StopWatch()
        _watcher.start()
        response = requests.get(url)
        logger.debug(f"response={response}")
        _watcher.stop()
        elapsed = _watcher.elapsed()
        logger.debug(f"elapsed={elapsed}")
        ttfb = elapsed * 1000  # Convert to milliseconds

        logger.debug(f"-measure_ttfb(), url={url}, ttfb={ttfb}")
        return ttfb
