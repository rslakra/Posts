from json import JSONDecodeError

from fastapi import Request
import logging

logger = logging.getLogger(__name__)


class BaseRouter:
    """BaseRouter provides shared request helper methods for route classes."""

    @staticmethod
    def query_params(request: Request) -> dict:
        """Convert request query params to a plain dictionary."""
        return dict(request.query_params)

    @staticmethod
    async def json_or_none(request: Request):
        """Return parsed JSON body, or None when body is absent/non-JSON."""
        try:
            return await request.json()
        except JSONDecodeError:
            logger.debug("json_or_none(): request body is empty or invalid JSON")
            return None
        except Exception as ex:
            logger.warning(f"json_or_none(): unable to parse request JSON, error={ex}")
            return None

    @staticmethod
    async def payload_or_none(request: Request):
        """Return request payload from form-data/urlencoded or JSON body."""
        content_type = request.headers.get("content-type", "")
        if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
            try:
                return dict(await request.form())
            except Exception as ex:
                logger.warning(f"payload_or_none(): unable to parse request form, error={ex}")
                return None

        return await BaseRouter.json_or_none(request)
