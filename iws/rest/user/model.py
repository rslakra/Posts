#
# Author: Rohtash Lakra
#
import logging
from dataclasses import field
from datetime import datetime
from typing import Optional, List, Any

from framework.orm.pydantic.model import AbstractModel, BaseModel

logger = logging.getLogger(__name__)


class Person(BaseModel):
    """Person contains properties specific to this object."""

    email: str = None
    first_name: str = None
    last_name: str = None
    birth_date: str | None = None

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"email={self.email!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, birth_date={self.birth_date!r}>"


class User(Person):
    """User contains properties specific to this object."""

    user_name: str = None
    password: str = None
    admin: bool | None = False
    last_seen: datetime | None = None
    avatar_url: str | None = None

    user_security: Optional["UserSecurity"] = None

    # roles: Optional[List["Role"]] = None
    addresses: Optional[List["Address"]] = field(default_factory=list)

    authenticated: bool = False

    def isAuthenticated(self) -> bool:
        return self.authenticated

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{self.getClassName()} => type={type(self)}, object={str(self)}")
        return self.model_dump_json()

    def toJSONObject(self) -> Any:
        # return {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}
        logger.debug(f"+toJSONObject() => type={type(self)}, object={str(self)}")
        jsonObject = self.model_dump(mode="json", exclude="user_security")
        # return self.model_dump(mode="json", exclude="user_security")
        logger.debug(f"-toJSONObject(), jsonObject={jsonObject}")
        return jsonObject

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return (
            "{} <id={}, email={}, user_name={}, first_name={}, last_name={}, admin={}, {}, user_security={}, addresses={}>"
            .format(self.getClassName(), self.id, self.email, self.user_name, self.first_name,
                    self.last_name, self.admin, self._auditable(), self.user_security, self.addresses))


class LoginUser(AbstractModel):
    """LoginUser contains properties specific to this object."""

    email: str = None
    user_name: str = None
    password: str = None


class UserSecurity(AbstractModel):
    """UserSecurity contains properties specific to this object."""

    user_id: int | None = None
    # user: User | None = None
    platform: str = None
    salt: str = None
    hashed_auth_token: str = None
    expire_at: datetime | None = None
    meta_data: dict | None = None

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <user_id={}, platform={}, salt={}, hashed_auth_token={}, expire_at={}, meta_data={}, {}>"
                .format(self.getClassName(), self.user_id, self.platform, self.salt, self.hashed_auth_token,
                        self.expire_at, self.meta_data, self._auditable()))


class Address(BaseModel):
    """Address contains properties specific to this object."""

    user_id: int | None = None
    user: User = None
    street1: str = None
    street2: str | None = None
    city: str = None
    state: str = None
    country: str = None
    zip: str = None

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{self.getClassName()} => type={type(self)}, object={str(self)}")
        return self.model_dump_json()

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{self.getClassName()} <id={self.id!r}, user_id={self.user_id!r}, street1={self.street1!r}, street2={self.street2!r}, city={self.city!r}, state={self.state!r}, country={self.country!r}, zip={self.zip!r}, {super()._auditable()}>"
