#
# Author: Rohtash Lakra
#
import json
from datetime import datetime
from typing import Protocol


class AbstractEntity(Protocol):
    """
     Define module-level constructs that will form the structures which we will be querying from the database.
     This structure, known as a Declarative Mapping, defines at once both a Python object model, and database
     metadata that describes real SQL tables that exist, or will exist, in a particular database:

    The mapping starts with a base class, which above is called 'AbstractEntity', and is created by making a simple
    subclass against the 'DeclarativeBase' class.

    Individual mapped classes are then created by making subclasses of 'AbstractEntity'.
    A mapped class typically refers to a single particular database table, the name of which is indicated by using
    the '__tablename__' class-level attribute.

    Normally, when one would like to map two different subclasses to individual tables, and leave the base class
    unmapped, this can be achieved very easily. When using Declarative, just declare the base class with
    the '__abstract__' indicator:
    """

    # def __getattr__(self, key):
    #     return self[key]
    #
    # def __setattr__(self, key, value):
    #     self[key] = value

    def default(o):
        return o.__dict__

    def to_json(self) -> str:
        return json.dumps(self.__dict__)


class BaseEntity(AbstractEntity):

    def __init__(self, id: int = None):
        """
        Alternatively, the same Table objects can be used in fully “classical” style, without using Declarative at all.
        A constructor similar to that supplied by Declarative is illustrated:
        """
        AbstractEntity.__init__(self)
        self.id = id

    def set_attrs(self, **kwargs):
        """
        Alternatively, the same Table objects can be used in fully “classical” style, without using Declarative at all.
        A constructor similar to that supplied by Declarative is illustrated:
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])

    # def json(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class NamedEntity(BaseEntity):

    def __init__(self, id: int, name: str):
        """
        Alternatively, the same Table objects can be used in fully “classical” style, without using Declarative at all.
        A constructor similar to that supplied by Declarative is illustrated:
        """
        BaseEntity.__init__(self, id)
        self.name = name

    # def json(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Role(NamedEntity):

    def __init__(self,
                 name: str,
                 id: int = None,
                 active: bool = True,
                 meta_data: str = None,
                 created_at: datetime = datetime.now(),
                 updated_at: datetime = datetime.now()):
        NamedEntity.__init__(self, id, name)
        self.active = active
        self.meta_data = meta_data
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"Role <id={self.id}, name={self.name}, active={self.active}, created_at={self.created_at}, updated_at={self.updated_at}>"

    # def json(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_json(self) -> str:
        return json.dumps(self, sort_keys=True, indent=4)


class Address(BaseEntity):

    def __init__(self,
                 street1: str,
                 city: str,
                 state: str,
                 country: str,
                 zip: str,
                 id: int = None,
                 user_id: int = None,
                 street2: str = None,
                 created_at: datetime = datetime.now(),
                 updated_at: datetime = datetime.now()):
        BaseEntity.__init__(self, id)
        self.user_id = user_id
        self.street1 = street1
        self.street2 = street2
        self.city = city
        self.state = state
        self.country = country
        self.zip = zip
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"Address <id={self.id}, user_id={self.user_id}, street1={self.street1}, street2={self.street2}, city={self.city}, state={self.state}, country={self.country}, zip={self.zip}, created_at={self.created_at}, updated_at={self.updated_at}>"


class User(BaseEntity):

    def __init__(self,
                 user_name: str,
                 password: str,
                 email: str,
                 first_name: str,
                 last_name: str,
                 id: int = None,
                 admin: bool = False,
                 created_at: datetime = datetime.now(),
                 updated_at: datetime = datetime.now(),
                 addresses: list[Address] = None):
        BaseEntity.__init__(self, id)
        self.user_name = user_name
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.admin = admin
        self.created_at = created_at
        self.updated_at = updated_at
        self.addresses: [Address] = [] if addresses is None else list(addresses)

    def add_address(self, address: Address):
        self.addresses.append(address)

    def __repr__(self) -> str:
        return f"User <id={self.id}, user_name={self.user_name}, email={self.email}, first_name={self.first_name}, last_name={self.last_name}, admin={self.admin}, created_at={self.created_at}, updated_at={self.updated_at}>"


class UserRole(BaseEntity):
    def __init__(self,
                 role_id: str,
                 user_id: str,
                 id: int = None,
                 active: bool = True,
                 created_at: datetime = datetime.now(),
                 updated_at: datetime = datetime.now()):
        BaseEntity.__init__(self, id)
        self.role_id = role_id
        self.user_id = user_id
        self.active = active
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"UserRole <id={self.id}, role_id={self.role_id}, user_id={self.user_id}, active={self.active}, created_at={self.created_at}, updated_at={self.updated_at}>"
