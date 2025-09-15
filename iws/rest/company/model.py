#
# Author: Rohtash Lakra
#

import logging
from typing import Optional, List, Any

from pydantic import model_validator
from typing_extensions import Self

from framework.orm.pydantic.model import NamedModel

logger = logging.getLogger(__name__)


class Company(NamedModel):
    """Role contains properties specific to this object."""

    # not Optional[], therefore will be NOT NULL except for the parent entity
    parent_id: int | None = None
    # not Optional[], therefore will be NOT NULL
    branches: Optional[List["Company"]] = None
    # not Optional[], therefore will be NOT NULL
    active: bool = False

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{self.getClassName()} => type={type(self)}, object={str(self)}")
        return self.model_dump_json()

    @model_validator(mode="before")
    @classmethod
    def preValidator(cls, values: Any) -> Any:
        logger.debug(f"preValidator({values})")
        return values

    @model_validator(mode="after")
    def postValidator(self, values) -> Self:
        logger.debug(f"postValidator({values})")
        return self

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, parent_id={}, name={}, active={}, {}>"
                .format(self.getClassName(), self.id, self.parent_id, self.name, self.active, self._auditable()))

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
