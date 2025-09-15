#
# Author: Rohtash Lakra
#
from typing import Optional, List

from sqlalchemy import PickleType, JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from framework.orm.sqlalchemy.schema import AbstractSchema, NamedSchema

"""
S = Subject = A person or automated agent
R = Role = Job function or title which defines an authority level
P = Permissions = An approval of a mode of access to a resource

A subject can have multiple roles.
A role can have multiple subjects.
A role can have many permissions.
A permission can be assigned to many roles.
An operation can be assigned to many permissions.
A permission can be assigned to many operations.

Setting uselist=False for non-annotated configurations
When using 'relationship()' without the benefit of Mapped annotations, the 'one-to-one' pattern can be enabled using the 
'relationship.uselist' parameter set to False on what would normally be the “many” side
"""


class RoleSchema(NamedSchema):
    """ RoleSchema represents [roles] Table

    Role = Job function or title which defines an authority level
    A role can have multiple subjects.
    A role can have many permissions.
    """

    __tablename__ = "roles"

    # not Optional[], therefore will be NOT NULL
    active: Mapped[bool] = mapped_column(unique=False, default=False)

    # Optional[], therefore will be NULL
    meta_data: Mapped[Optional[PickleType]] = mapped_column(JSON)

    # Define the many-to-many relationship
    # permissions: Mapped[List["PermissionSchema"]] = relationship(secondary="role_permissions")
    permissions: Mapped[Optional[List["PermissionSchema"]]] = relationship('PermissionSchema',
                                                                           secondary="role_permissions",
                                                                           lazy="joined")

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, name={}, active={}, meta_data={}, permissions={}, {}>"
                .format(self.getClassName(),
                        self.id,
                        self.name,
                        self.active,
                        self.meta_data,
                        self.permissions,
                        self.auditable()))


class PermissionSchema(NamedSchema):
    """ PermissionSchema represents [roles] Table

    Permissions = An approval of a mode of access to a resource.
    A permission can be assigned to many roles.
    A permission can be assigned to many operations.
    """

    __tablename__ = "permissions"

    # Optional[], therefore will be NULL
    description: Mapped[Optional[str]] = mapped_column(String(128))

    # not Optional[], therefore will be NOT NULL
    active: Mapped[bool] = mapped_column(unique=False, default=False)

    # Define the many-to-many relationship
    # roles: Mapped[List["RoleSchema"]] = relationship('RoleSchema', secondary="role_permissions", lazy="joined")

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, name={}, description={}, active={}, {}>"
                .format(self.getClassName(),
                        self.id,
                        self.name,
                        self.description,
                        self.active,
                        self.auditable()))


class RolePermissionSchema(AbstractSchema):
    """ RolePermissionSchema represents [user_roles] Table """

    __tablename__ = "role_permissions"

    # foreign key to "roles.id" and "users.id" are added
    # not Optional[], therefore will be NOT NULL
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    # Define the many-to-one relationship
    # association between Association -> Role
    role: Mapped["RoleSchema"] = relationship("RoleSchema", overlaps="permissions")

    # not Optional[], therefore will be NOT NULL
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"), primary_key=True)
    # Define the many-to-one relationship
    # association between Association -> Permission
    permission: Mapped["PermissionSchema"] = relationship("PermissionSchema", overlaps="permissions")

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, role_id={}, permission_id={}, {}>"
                .format(self.getClassName(), self.id, self.role_id, self.permission_id, self.auditable()))


class CapabilitySchema(NamedSchema):
    """ CapabilitySchema represents [roles] Table

    Capability = refers the action allowed to a resource.
    A capability can be assigned to many roles.
    A capability can be assigned to many operations.
    """

    __tablename__ = "capabilities"

    # Optional[], therefore will be NULL
    description: Mapped[Optional[str]] = mapped_column(String(128))

    # not Optional[], therefore will be NOT NULL
    active: Mapped[bool] = mapped_column(unique=False, default=False)

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, name={}, description={}, active={}, {}>"
                .format(self.getClassName(),
                        self.id,
                        self.name,
                        self.description,
                        self.active,
                        self.auditable()))
