#
# Author: Rohtash Lakra
#
from sqlalchemy import String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from framework.orm.sqlalchemy.entity import BaseEntity


class Document(BaseEntity):
    """
    [documents] Table
    """
    __tablename__ = "documents"

    # foreign key to "users.id" is added
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # user: Mapped["User"] = relationship(back_populates="addresses")

    filename: Mapped[str] = mapped_column(String(64))
    data: Mapped[LargeBinary] = mapped_column(LargeBinary)

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"Document <id={self.id!r}, filename={self.filename!r}, data=*, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


#
# Author: Rohtash Lakra
#
from framework.orm.pydantic.entity import BaseEntity


class Document(BaseEntity):

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, id: int = None, filename: str = None, data: str = None):
        super().__init__(id)
        self.filename = filename
        self.data = data

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{self.getClassName()} <id={self.id}, filename={self.filename}, data={self.data}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
