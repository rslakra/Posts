#
# Author: Rohtash Lakra
# References:
# - https://docs.sqlalchemy.org/en/20/orm/self_referential.html
#
from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from framework.orm.sqlalchemy.schema import NamedSchema


class CompanySchema(NamedSchema):
    """ CompanySchema represents [companies] Table """

    __tablename__ = "companies"

    # foreign key to "companies.id" is added
    # not Optional[], therefore will be NOT NULL except for the parent entity
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("companies.id"))

    # not Optional[], therefore will be NOT NULL
    # the parent and its immediate child collection or reference can be populated from a single SQL statement
    branches: Mapped[List[Optional["CompanySchema"]]] = relationship("CompanySchema", lazy="joined", join_depth=2)

    # not Optional[], therefore will be NOT NULL
    active: Mapped[bool] = mapped_column(unique=False, default=False)

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, parent_id={}, name={}, active={}, {}>"
                .format(self.getClassName(), self.id, self.parent_id, self.name, self.active, self.auditable()))

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
