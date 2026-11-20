#
# Author: Rohtash Lakra
#
import functools
import inspect
import json
import typing as t
import uuid
from datetime import datetime as dt
from decimal import Decimal

from sqlalchemy.orm import DeclarativeMeta


def wrap_default(default_fn: t.Callable) -> t.Callable:
    """The Connexion defaults for JSON encoding. Handles extra types compared to the
    built-in :class:`json.JSONEncoder`.

    -   :class:`datetime.datetime` and :class:`datetime.date` are
        serialized to :rfc:`822` strings. This is the same as the HTTP
        date format.
    -   :class:`decimal.Decimal` is serialized to a float.
    -   :class:`uuid.UUID` is serialized to a string.
    """

    @functools.wraps(default_fn)
    def wrapped_default(self, o):
        if isinstance(o, dt):
            if o.tzinfo:
                # eg: '2015-09-25T23:14:42.588601+00:00'
                return o.isoformat("T")
            else:
                # No timezone present - assume UTC.
                # eg: '2015-09-25T23:14:42.588601Z'
                return o.isoformat("T") + "Z"

        if isinstance(o, dt.date):
            return o.isoformat()

        if isinstance(o, Decimal):
            return float(o)

        if isinstance(o, uuid.UUID):
            return str(o)

        return default_fn(self, o)

    return wrapped_default


class JSONEncoder(json.JSONEncoder):
    """The default Connexion JSON encoder. Handles extra types compared to the
    built-in :class:`json.JSONEncoder`.

    -   :class:`datetime.datetime` and :class:`datetime.date` are
        serialized to :rfc:`822` strings. This is the same as the HTTP
        date format.
    -   :class:`uuid.UUID` is serialized to a string.
    """

    @wrap_default
    def default(self, instance):
        return super().default(instance)


class JSONUtils:
    """ Central point to serialize and deserialize to/from JSON. """

    def __init__(self, json_=json, **kwargs):
        """
        :param json_: json library to use. Must have loads() and dumps() method  # NOQA
        :param kwargs: default arguments to pass to json.dumps()
        """
        self.json = json_
        self.dumps_args = kwargs
        self.dumps_args.setdefault("cls", JSONEncoder)

    def dumps(self, data, **kwargs):
        """Central point where JSON serialization happens inside
        Connexion.
        """
        for k, v in self.dumps_args.items():
            kwargs.setdefault(k, v)
        return self.json.dumps(data, **kwargs) + "\n"

    def loads(self, data):
        """Central point where JSON deserialization happens inside
        Connexion.
        """
        if isinstance(data, bytes):
            data = data.decode()

        try:
            return self.json.loads(data)
        except Exception:
            if isinstance(data, str):
                return data


class JsonEncoder(JSONEncoder):

    @wrap_default
    def default(self, o):
        return super().default(o)

    def default(self, instance):
        # return super().default(instance)
        if hasattr(instance, "to_json"):
            return self.default(instance.to_json())
        elif hasattr(instance, "__dict__"):
            obj_dict = dict((key, value) for key, value in inspect.getmembers(instance)
                            if not key.startswith("__")
                            and not inspect.isabstract(value)
                            and not inspect.isbuiltin(value)
                            and not inspect.isfunction(value)
                            and not inspect.isgenerator(value)
                            and not inspect.isgeneratorfunction(value)
                            and not inspect.ismethod(value)
                            and not inspect.ismethoddescriptor(value)
                            and not inspect.isroutine(value)
                            )
            return self.default(obj_dict)

        return instance


class AbstractJSONHandler(JSONEncoder):
    """AbstractJSONHandler extends JSONEncoder"""

    # skip JSONEncoder properties
    _jsonEncKeys = ('skipkeys', 'ensure_ascii', 'check_circular', 'allow_nan', 'sort_keys', 'indent')

    def _skipDefaultKeys(self, entity):
        # skip JSONEncoder properties
        for key in AbstractJSONHandler._jsonEncKeys:
            if key in entity.__dict__:
                # print(f"key: {key}")
                entity.__delattr__(key)
        # print(f"entity.__dict__: {entity.__dict__}")

    def default(self, entity):
        """
        Implement this method in a subclass such that it returns
                a serializable object for ``o``, or calls the base implementation
                (to raise a ``TypeError``).
        """

        if isinstance(entity, AbstractJSONHandler):
            # JSONEncoder.default() must return a JSON-serializable Python object
            # (dict/list/scalar), not an already encoded JSON string.
            #
            # Historical note:
            # This method previously returned `json.dumps(...)` here. That worked for
            # debug prints, but API responses started returning quoted JSON strings
            # (double-encoded payloads). We now return a plain dict and let callers
            # choose when to render a JSON string.
            payload = dict(entity.__dict__)
            for key in AbstractJSONHandler._jsonEncKeys:
                payload.pop(key, None)
            return payload

        # Let the base class default method raise the TypeError
        return super().default(entity)


class DefaultJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class and exclude metadata
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                try:
                    data = obj.__getattribute__(field)
                    if isinstance(data, dt):  # handle datatime
                        data = data.isoformat()

                    json.dumps(data)  # jsonify the field's data and failed if not encoded
                    fields[field] = data
                except TypeError:
                    fields[field] = None

            # a json-encoder dict
            return fields

        return JSONEncoder.default(self, obj)


# def recursive_encoder():
#     # _visited = []

class RecursiveJSONEncoder(DefaultJSONEncoder):
    _visited = []

    def default(self, instance):
        if isinstance(instance.__class__, DeclarativeMeta):
            # avoid self re-visit
            if instance in self._visited:
                return None

            # mark visited
            self._visited.append(instance)

            # an SQLAlchemy class and exclude metadata
            fields = {}
            for field in [x for x in dir(instance) if not x.startswith('_') and x != 'metadata']:
                try:
                    data = instance.__getattribute__(field)
                    if isinstance(data, dt):  # handle datatime
                        data = data.isoformat()

                    json.dumps(data)  # jsonify the field's data and failed if not encoded
                    fields[field] = data
                except TypeError:
                    fields[field] = None

            # a json-encoder dict
            return fields

        return json.JSONEncoder.default(self, instance)

# return RecursiveJ/SONEncoder
