#
# Author: Rohtash Lakra
#
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, ForeignKey, func, PickleType, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from framework.orm.sqlalchemy.schema import AbstractSchema, BaseSchema


class PersonSchema(BaseSchema):
    """ PersonSchema represents the person object """

    __abstract__ = True

    # not Optional[], therefore will be NOT NULL
    email: Mapped[str] = mapped_column(String(128), unique=True)
    # not Optional[], therefore will be NOT NULL
    first_name: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    last_name: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    birth_date: Mapped[str] = mapped_column(String(10), nullable=False)
    # not Optional[], therefore will be NOT NULL
    avatar_url: Mapped[Optional[str]] = mapped_column(String(128))

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, email={}, first_name={}, last_name={}, birth_date={}, avatar_url={}, {}>"
                .format(self.getClassName(), self.id, self.email, self.first_name, self.last_name, self.birth_date,
                        self.avatar_url, self.auditable()))


class UserSchema(PersonSchema):
    """ UserSchema represents [users] Table """

    __tablename__ = "users"

    # not Optional[], therefore will be NOT NULL
    user_name: Mapped[str] = mapped_column(String(64), unique=True)
    # not Optional[], therefore will be NOT NULL
    admin: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    # Optional[], therefore will be NULL
    last_seen: Mapped[Optional[datetime]] = mapped_column(insert_default=func.now())

    # not Optional[], therefore will be NOT NULL
    # 'one-to-one' pattern can be enabled using the 'relationship.uselist' parameter set to 'False'
    user_security: Mapped["UserSecuritySchema"] = relationship("UserSecuritySchema", back_populates="user",
                                                               lazy="joined", uselist=False,
                                                               cascade="all, delete-orphan")

    # Other variants of 'Mapped' are available, most commonly the 'relationship()' construct indicated above.
    # In contrast to the column-based attributes, 'relationship()' denotes a linkage between two ORM classes.
    # addresses: Mapped[List["Role"]] = relationship(back_populates="role", cascade="all, delete-orphan")
    # Optional[], therefore will be NULL
    # roles: Mapped[List["Role"]] = relationship(back_populates="role", cascade="all, delete-orphan")
    # roles: Mapped[List["UserRoleSchema"]] = relationship(back_populates="roles", cascade="all, delete-orphan", secondary="users")

    # Other variants of 'Mapped' are available, most commonly the 'relationship()' construct indicated above.
    # In contrast to the column-based attributes, 'relationship()' denotes a linkage between two ORM classes.
    # addresses: Mapped[List["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    # Optional[], therefore will be NULL
    # Define the one-to-many relationship
    addresses: Mapped[Optional[List["AddressSchema"]]] = relationship(back_populates="user", lazy="joined",
                                                                      cascade="all, delete-orphan")

    # Define the one-to-many relationship
    # sessions: Mapped[List["UserSessionSchema"]] = relationship(back_populates="user")

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return (
            "{} <id={}, email={}, first_name={}, last_name={}, user_name={}, admin={}, last_seen={}, {}, user_security={}, addresses={}>"
            .format(self.getClassName(), self.id, self.email, self.first_name, self.last_name, self.user_name,
                    self.admin, self.last_seen, self.auditable(), self.user_security, self.addresses))


class UserSecuritySchema(AbstractSchema):
    """ UserSecuritySchema represents [user_sessions] Table """

    __tablename__ = "user_securities"

    # foreign key to "users.id" is added
    # not Optional[], therefore will be NOT NULL
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    # Define the one-to-one relationship
    user: Mapped["UserSchema"] = relationship("UserSchema", back_populates="user_security")

    # not Optional[], therefore will be NOT NULL
    platform: Mapped[str] = mapped_column(String(64))

    # not Optional[], therefore will be NOT NULL
    salt: Mapped[str] = mapped_column(String(32))

    # not Optional[], therefore will be NOT NULL
    hashed_auth_token: Mapped[str] = mapped_column(String(128))

    # Optional[], therefore will be NULL
    expire_at: Mapped[Optional[str]] = mapped_column(String(64))

    # Optional[], therefore will be NULL
    meta_data: Mapped[Optional[PickleType]] = mapped_column(JSON)

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <user_id={}, platform={}, salt={}, hashed_auth_token={}, expire_at={}, meta_data={}, {}>"
                .format(self.getClassName(), self.user_id, self.platform, self.salt, self.hashed_auth_token,
                        self.expire_at, self.meta_data, self.auditable()))


class UserRoleSchema(AbstractSchema):
    """ UserRoleSchema represents [user_roles] Table """

    __tablename__ = "user_roles"

    # foreign key to "roles.id" and "users.id" are added
    # not Optional[], therefore will be NOT NULL
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    # not Optional[], therefore will be NOT NULL
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    # Define the many-to-one relationship
    role: Mapped["RoleSchema"] = relationship("RoleSchema")
    user: Mapped["UserSchema"] = relationship("UserSchema")

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, role_id={}, user_id={}, {}>"
                .format(self.getClassName(), self.id, self.role_id, self.user_id, self.auditable()))


class AddressSchema(BaseSchema):
    """ AddressSchema represents [addresses] Table """

    __tablename__ = "addresses"

    # foreign key to "users.id" is added
    # not Optional[], therefore will be NOT NULL
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # Define the many-to-one relationship
    user: Mapped["UserSchema"] = relationship(back_populates="addresses")

    # not Optional[], therefore will be NOT NULL
    street1: Mapped[str] = mapped_column(String(64))
    # Optional[], therefore will be NULL
    street2: Mapped[Optional[str]] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    city: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    state: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    country: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    zip: Mapped[str] = mapped_column(String(16))

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, user_id={}, street1={}, street2={}, city={}, state={}, country={}, zip={}, {}>"
                .format(self.getClassName(), self.id, self.user_id, self.street1, self.street2, self.city,
                        self.state, self.country, self.zip, self.auditable()))
