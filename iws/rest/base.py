from json import JSONDecodeError

from fastapi import Request


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
            return None
