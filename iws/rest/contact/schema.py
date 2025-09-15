#
# Author: Rohtash Lakra
#

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from framework.orm.sqlalchemy.schema import BaseSchema


class ContactSchema(BaseSchema):
    """ ContactSchema represents [contacts] Table """

    __tablename__ = "contacts"

    # not Optional[], therefore will be NOT NULL
    first_name: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    last_name: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    country: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    subject: Mapped[str] = mapped_column(String(64))

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, first_name={}, last_name={}, country={}, subject={}, {}>"
                .format(self.getClassName(),
                        self.id,
                        self.first_name,
                        self.last_name,
                        self.country,
                        self.subject,
                        self.auditable()))

    # def __repr__(self) -> str:
    #     """Returns the string representation of this object"""
    #     return str(self)
