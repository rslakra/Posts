#
# Author: Rohtash Lakra
#

import logging
from dataclasses import field
from typing import Dict, Any, List, Optional

from pydantic import model_validator
from typing_extensions import Self

from framework.orm.pydantic.model import AbstractModel, NamedModel

logger = logging.getLogger(__name__)


class Role(NamedModel):
    """Role contains properties specific to this object."""

    active: bool = False
    meta_data: Dict[str, Any] | None = None
    permissions: Optional[List["Permission"]] = field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def preValidator(cls, values: Any) -> Any:
        logger.debug(f"preValidator({values})")
        return super().preValidator(values)

    @model_validator(mode="after")
    def postValidator(self, values) -> Self:
        logger.debug(f"postValidator({values})")
        return super().postValidator(values)

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{self.getClassName()} => type={type(self)}, object={str(self)}")
        return self.model_dump_json()

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, name={}, active={}, meta_data={}, permissions={}, {}>"
                .format(self.getClassName(),
                        self.id,
                        self.name,
                        self.active,
                        self.meta_data,
                        self.permissions,
                        self._auditable()))


class Permission(NamedModel):
    """Permission contains properties specific to this object."""

    description: Optional[str] = None
    active: bool = False

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{self.getClassName()} => type={type(self)}, object={str(self)}")
        return self.model_dump_json()

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, name={}, description={}, active={}, {}>"
                .format(self.getClassName(),
                        self.id,
                        self.name,
                        self.description,
                        self.active,
                        self._auditable()))


class Capability(NamedModel):
    """Capability contains properties specific to this object."""

    description: Optional[str] = None
    active: bool = False

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{self.getClassName()} => type={type(self)}, object={str(self)}")
        return self.model_dump_json()

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, name={}, active={}, meta_data={}, {}>"
                .format(self.getClassName(),
                        self.id,
                        self.name,
                        self.description,
                        self.active,
                        self._auditable()))


class RoleAssignPermission(AbstractModel):
    """Role contains properties specific to this object."""
    role_id: int
    permissions: Optional[List[int]] = field(default_factory=list)

    def _validate(cls, values: dict) -> Any:
        if isinstance(values, dict):
            if 'role_id' not in values:
                raise ValueError("'role_id' should provide!")
            if 'permissions' not in values or not values.get("permissions"):
                raise ValueError("'permissions' should provide!")

        return values

    @model_validator(mode="before")
    @classmethod
    def preValidator(cls, values: Any) -> Any:
        logger.debug(f"+preValidator(), values={values}")
        # <class 'pydantic._internal._model_construction.ModelMetaclass'>
        if isinstance(values, list):
            for value in values:
                cls._validate(cls, value)
        if isinstance(values, dict):
            cls._validate(cls, values)

        return values

    @model_validator(mode="after")
    def postValidator(self, values) -> Self:
        logger.debug(f"postValidator({values})")
        return super().postValidator(values)

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{self.getClassName()} => type={type(self)}, object={str(self)}")
        return self.model_dump_json()

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <role_id={}, permissions={}>"
                .format(self.getClassName(), self.role_id, self.permissions))
