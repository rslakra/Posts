#
# Author: Rohtash Lakra
#
import logging
from typing import Any

from pydantic import model_validator
from typing_extensions import Self

from framework.orm.pydantic.model import BaseModel

logger = logging.getLogger(__name__)


class Contact(BaseModel):
    """Contact contains properties specific to this object."""

    first_name: str = None
    last_name: str = None
    country: str = None
    subject: str = None

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
        return ("{} <id={}, first_name={}, last_name={}, country={}, subject={}, {}>"
                .format(self.getClassName(),
                        self.id,
                        self.first_name,
                        self.last_name,
                        self.country,
                        self.subject,
                        self._auditable()))

    # def __repr__(self) -> str:
    #     """Returns the string representation of this object"""
    #     return str(self)

    @staticmethod
    def create(first_name, last_name, country, subject):
        """Creates the contact object with values"""
        print(f"first_name:{first_name}, last_name:{last_name}, country:{country}, subject:{subject}")
        return Contact(first_name=first_name, last_name=last_name, country=country, subject=subject)
