#
# Author: Rohtash Lakra
#
# References: -
# - https://docs.sqlalchemy.org/en/20/orm/quickstart.html
# - https://docs.sqlalchemy.org/en/20/orm/inheritance.html
#
from __future__ import annotations

import logging
from datetime import datetime
from enum import unique, auto
from math import ceil
from typing import Any

from sqlalchemy import func, orm, String, event, inspect
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.orm.query import attributes

from framework.enums import AutoUpperCase

logger = logging.getLogger(__name__)


@unique
class SchemaOperation(AutoUpperCase):
    """Entity Operations"""
    # Adds new data or records to the database
    CREATE = auto()
    # Removes data from the database
    DELETE = auto()
    # Retrieves data from the database
    READ = auto()
    # Modifies existing data in the database
    UPDATE = auto()


class Pagination(object):
    """Pagination Class is returned by `Query.paginate`. You can also construct it from any other SQLAlchemy query
    object if you are working with other libraries. Additionally, it is possible to pass ``None`` as query object in
    which case the `prev` and `next` will no longer work.
    """

    def __init__(self, query, page: int, page_size: int, total: int, items):
        logger.debug(f"+Pagination({query}, {page}, {page_size}, {total})")

        #: The query object that was used to create this pagination object.
        self.query = query
        #: The current page number (1 indexed).
        self.page = page
        #: The number of items to be displayed on a page.
        self.page_size = page_size
        #: The total number of items matching the query.
        self.total = total
        #: The items for the current page.
        self.items = items
        if self.page_size == 0:
            self.pages = 0
        else:
            #: The total number of pages.
            self.pages = int(ceil(self.total / float(self.page_size)))
        #: Number of the previous page.
        self.prev_page = self.page - 1
        #: True if a previous page exists.
        self.has_prev = self.page > 1
        #: Number of the next page.
        self.next_page = self.page + 1
        #: True if a next page exists.
        self.has_next = self.page < self.pages
        logger.debug(f"-Pagination()")

    def prev(self, throw_error: bool = False):
        """Returns a `Pagination` object for the previous page."""
        assert self.query is not None, 'a query object is required for this method to work'
        return self.query.paginate(self.page - 1, self.page_size, throw_error)

    def next(self, throw_error: bool = False):
        """Returns a `Pagination` object for the next page."""
        assert self.query is not None, 'a query object is required for this method to work'
        return self.query.paginate(self.page + 1, self.per_page, throw_error)


class BaseQuery(orm.Query):
    """The query class is either SQLAlchemy’s orm.Query class or a child class that inherits from it.
    The query property is what allows the 'Model.query' style access and is easy to create, but does require access to
    the database session when setting up.

    The default query object used for models. This can be subclassed and replaced for individual models by setting
    the 'Model.query_class' attribute. This is a subclass of a standard SQLAlchemy 'sqlalchemy.orm.query.Query' class,
    and has all the methods of a standard query as well.
    """

    def __init__(self):
        # super().__init__(entities=None)
        self.DEFAULT_PER_PAGE = 20

    def paginate(self, page: int, page_size: int = 20, throw_error: bool = True):
        """Return `Pagination` instance using already defined query parameters.
        """
        logger.debug(f"+paginate({page}, {page_size}, {throw_error})")
        if throw_error and page < 1:
            raise IndexError

        if page_size is None:
            page_size = self.DEFAULT_PER_PAGE

        items = self.page(page, page_size).all()
        if not items and page != 1 and throw_error:
            raise IndexError

        # No need to count if we're on the first page and there are fewer items than we expected.
        if page == 1 and len(items) < page_size:
            total = len(items)
        else:
            total = self.order_by(None).count()

        pagination = Pagination(self, page, page_size, total, items)
        logger.debug(f"-paginate(), pagination={pagination}")
        return pagination


class QueryProperty(object):
    """Query property accessor which gives the model access to query capabilities via `BaseModel.query` which is
    equivalent to ``session.query(Model)``.

    For the query property functionality, we need to define this query property class.
    """

    def __init__(self, session):
        self.session = session

    def __get__(self, model, AbstractSchema):
        mapper = orm.class_mapper(AbstractSchema)
        if mapper:
            if not getattr(AbstractSchema, 'query_class', None):
                AbstractSchema.query_class = BaseQuery
            query_property = AbstractSchema.query_class(mapper, session=self.session())

            return query_property


class Serializable(object):
    __exclude__ = ('id',)
    __include__ = ()
    __write_only__ = ()

    @classmethod
    def from_json(cls, json, instance=None):
        self = cls() if instance is None else instance
        exclude = (cls.__exclude__ or ()) + Serializable.__exclude__
        include = cls.__include__ or ()

        if json:
            for key, value in json.iteritems():
                # ignore all non user data, e.g. only
                if (not (key in exclude) | (key in include)) and isinstance(getattr(cls, key, None),
                                                                            attributes.QueryableAttribute):
                    setattr(self, key, value)

        return self

    def deserialize(self, json):
        return self.__class__.from_json(json, instance=self) if json else None

    @classmethod
    def serialize_list(cls, instances=[]):
        output = []
        for instance in instances:
            if isinstance(instance, Serializable):
                output.append(instance.serialize())
            else:
                output.append(instance)

        return output

    def serialize(self, **kwargs):
        # init write only props
        if len(getattr(self.__class__, '__write_only__', ())) == 0:
            self.__class__.__write_only__ = ()

        dictionary = {}
        expand = kwargs.get('expand', ()) or ()
        key = 'props'

        if expand:
            # expand all the fields
            for key in expand:
                getattr(self, key)

        iterable = self.__dict__.items()
        is_custom_property_set = False

        # include only properties passed as parameter
        if (key in kwargs) and (kwargs.get(key, None) is not None):
            is_custom_property_set = True
            iterable = kwargs.get(key, None)

        # loop through all accessible properties
        for key in iterable:
            accessor = key
            if isinstance(key, tuple):
                accessor = key[0]

            if not (accessor in self.__class__.__write_only__) and not accessor.startswith('_'):
                # force select from db to get relationships
                if is_custom_property_set:
                    getattr(self, accessor, None)
                if isinstance(self.__dict__.get(accessor), list):
                    dictionary[accessor] = self.__class__.serialize_list(instances=self.__dict__.get(accessor))
                # check if those properties are read only
                elif isinstance(self.__dict__.get(accessor), Serializable):
                    dictionary[accessor] = self.__dict__.get(accessor).serialize()
                else:
                    dictionary[accessor] = self.__dict__.get(accessor)

        return dictionary


def set_query_property(model_class, session):
    """A helper method for attaching the query property to the model."""
    model_class.query = QueryProperty(session)


class AbstractSchema(DeclarativeBase):
    """
    AbstractSchema define module-level constructs that will form the structures which we will be querying from the
    database. This structure, known as a Declarative Mapping, defines at once both a Python object model, and database
    metadata that describes real SQL tables that exist, or will exist, in a particular database:

    The mapping starts with a base class, which above is called 'AbstractSchema', and is created by making a simple
    subclass against the 'DeclarativeBase' class.

    Individual mapped classes are then created by making subclasses of 'AbstractSchema'.
    A mapped class typically refers to a single particular database table, the name of which is indicated by using
    the '__tablename__' class-level attribute.

    Normally, when one would like to map two different subclasses to individual tables, and leave the base class
    unmapped, this can be achieved very easily. When using Declarative, just declare the base class with
    the '__abstract__' indicator:
    """
    __abstract__ = True

    # the query class used. The `query` attribute is an instance of this class. By default, a `BaseQuery` is used.
    query_class = BaseQuery

    # an instance of `query_class`. Can be used to query the database for instances of this model.
    query = None

    # not Optional[], therefore will be NOT NULL
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    # not Optional[], therefore will be NOT NULL
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())

    def __init__(self, **kwargs):
        """
        Alternatively, the same Table objects can be used in fully “classical” style, without using Declarative at all.
        A constructor similar to that supplied by Declarative is illustrated:
        """
        logger.debug(f"+{self.getClassName()}({kwargs})")
        self.setAttributes(**kwargs)
        logger.debug(f"-{self.getClassName()}()")

    def setAttributes(self, **kwargs):
        """
        Alternatively, the same Table objects can be used in fully “classical” style, without using Declarative at all.
        A constructor similar to that supplied by Declarative is illustrated:
        """
        logger.debug(f"+setAttributes({kwargs})")
        for key in kwargs:
            logger.debug(f"{key}={kwargs[key]}, ({type(kwargs[key])})")
            # handle error - AttributeError: 'dict' object has no attribute '_sa_instance_state'
            # setattr(self, key, kwargs[key])
            if isinstance(kwargs[key], list):
                # TODO: handle recursively copy objects of ORM objects.
                # self.setAttributes(**kwargs[key])
                pass
            else:
                setattr(self, key, kwargs[key])

        logger.debug(f"-setAttributes()")

    def getClassName(self) -> str:
        """Returns the name of the class."""
        return type(self).__name__

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{self.getClassName()} <{self.auditable()}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)

    def auditable(self) -> str:
        """Returns the string representation of this object"""
        return f"created_at={self.created_at}, updated_at={self.updated_at}>"

    def to_json(self) -> Any:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def toJSONObject(self) -> Any:
        return {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}


"""
Create the declarative base. This will become the common source for all future SQLAlchemy classes.
For example:
from .abstract import Model
class User(Model):
    # define user model
    pass

"""


# Model = declarative_base(cls=AbstractSchema)
# BaseSchema = declarative_base(cls=AbstractSchema)


class BaseSchema(AbstractSchema):
    """
    AbstractSchema define module-level constructs that will form the structures which we will be querying from the
    database. This structure, known as a Declarative Mapping, defines at once both a Python object model, and database
    metadata that describes real SQL tables that exist, or will exist, in a particular database:

    The mapping starts with a base class, which above is called 'BaseSchema', and is created by making a simple
    subclass against the 'DeclarativeBase' class.

    Individual mapped classes are then created by making subclasses of 'BaseSchema'.
    A mapped class typically refers to a single particular database table, the name of which is indicated by using
    the '__tablename__' class-level attribute.

    Normally, when one would like to map two different subclasses to individual tables, and leave the base class
    unmapped, this can be achieved very easily. When using Declarative, just declare the base class with
    the '__abstract__' indicator:
    """
    __abstract__ = True

    """
    ID - Primary Key

    All ORM mapped classes require at least one column be declared as part of the primary key, typically by using
    the 'Column.primary_key' parameter on those 'mapped_column()' objects that should be part of the key.
    """
    # primary_key=True, therefore will be NOT NULL
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return "{} <id={}, {}>".format(self.getClassName(), self.id, self.auditable())


@event.listens_for(BaseSchema.metadata, "column_reflect")
def column_reflect(inspector, table, column_info):
    # set column.key = "attr_<lower_case_name>"
    logger.info(f"column_reflect({table}, {column_info})")
    # column_info["key"] = "attr_%s" % column_info["name"].lower()


# @event.listens_for(BaseSchema, "after_insert")
# def after_insert(inspector, table, column_info):
#     # set column.key = "attr_<lower_case_name>"
#     logger.info(f"after_insert({table}, {column_info})")
#     # column_info["key"] = "attr_%s" % column_info["name"].lower()


class NamedSchema(BaseSchema):
    """NamedEntity Schema"""
    __abstract__ = True

    # not Optional[], therefore will be NOT NULL
    name: Mapped[str] = mapped_column(String(64), unique=True)
