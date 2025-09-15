#
# Author: Rohtash Lakra
#
import logging
from abc import abstractmethod
from typing import List, Optional, Dict, Any

from framework.orm.pydantic.model import BaseModel
from framework.orm.sqlalchemy.schema import SchemaOperation

logger = logging.getLogger(__name__)


class AbstractService(object):
    """
    An abstract service for all other services inherits.
    """

    def __init__(self):
        logger.debug("AbstractService()")
        pass

    def getClassName(self) -> str:
        """Returns the name of the class."""
        return type(self).__name__

    @abstractmethod
    def validate(self, operation: SchemaOperation, modelObject: BaseModel) -> None:
        logger.debug(f"validate({operation}, {modelObject})")
        pass

    @abstractmethod
    def findByFilter(self, filters: Dict[str, Any]) -> List[Optional[BaseModel]]:
        logger.debug(f"findByFilter({filters})")
        pass

    @abstractmethod
    def existsByFilter(self, filters: Dict[str, Any]) -> bool:
        logger.debug(f"existsByFilter({filters})")
        pass

    def load(schema_class, json, only=None, exclude=[], partial=False, many=False):
        return schema_class(only=only, exclude=exclude, partial=partial, many=many).load_and_not_raise(json)

    def validate(schema_class, json, only=None, exclude=[], partial=False, many=False):
        schema_class(only=only, exclude=exclude, partial=partial, many=many).validate_and_raise(json)

    def dump(schema_class, obj, only=None, exclude=[], partial=False, many=False):
        return schema_class(only=only, exclude=exclude, partial=partial, many=many).dump(obj)


class DataStore:

    def init(self, app):
        self.app = app

    @property
    def get_app(self):
        return self.app
