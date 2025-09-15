#
# Author: Rohtash Lakra
#
from framework.orm.pydantic.entity import BaseEntity


class User(BaseEntity):

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, id: int = None, user_name: str = None, password: str = None, first_name: str = None,
                 last_name: str = None, email: str = None, is_admin: bool = False):
        super().__init__(id)
        self.user_name = user_name
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.admin = is_admin

    def __repr__(self) -> str:
        return f"{self.getClassName()} <id={self.id}, user_name={self.user_name}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, admin={self.admin}>"
