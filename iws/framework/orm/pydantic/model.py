#
# Author: Rohtash Lakra
# Reference(s):
#  - https://docs.pydantic.dev/latest/
#
from __future__ import annotations

import json
import logging
from datetime import datetime
from enum import unique, auto
from typing import Optional, Dict, List, Any, Union

from pydantic import (
    BaseModel as PydanticBaseModel,
    ValidationError,
    ConfigDict,
    model_validator,
    field_validator
)
# from pydantic.alias_generators import (
#     to_camel,
#     to_pascal,
#     to_snake
# )
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

from framework.enums import BaseEnum
from framework.exception import (
    AbstractException,
    ValidationException,
    DuplicateRecordException,
    NoRecordFoundException
)
from framework.http import HTTPStatus
from framework.utils import Utils

logger = logging.getLogger(__name__)


@unique
class Status(BaseEnum):
    """Enum for Status. For readability, add constants in Alphabetical order."""
    CREATED = auto()
    DELETED = auto()
    UPDATED = auto()


@unique
class SyncStatus(BaseEnum):
    """Enum for SyncStatus. For readability, add constants in Alphabetical order."""
    COMPLETED = auto()
    FAILED = auto()
    IGNORED = auto()
    PENDING = auto()
    SCHEDULED = auto()


class ConfigSetting(BaseSettings):
    """ConfigSetting is a base model for all configuration parameters."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra="allow"
    )

    # class Config:
    #     env_file = ".env"
    #     case_sensitive = True
    #     extra = "allow"


class PydanticAbstractModel(PydanticBaseModel):
    """PydanticAbstractModel is a base model for all models inherit and provides basic configuration parameters."""

    # protected_namespaces=() disables the protected namespace validation
    # model_config = ConfigDict(from_attributes=True, validate_assignment=True, arbitrary_types_allowed=True,
    #                           use_enum_values=True, alias_generator=AliasGenerator(
    #         validation_alias=to_snake,
    #         serialization_alias=to_snake,
    #     ), protected_namespaces=())
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        protected_namespaces=()
    )

    def getClassName(self) -> str:
        """Returns the name of the class."""
        return type(self).__name__

    def getAllFields(self, alias=False) -> list:
        # return list(self.schema(by_alias=alias).get("properties").keys())
        return list(self.model_json_schema(by_alias=alias).get("properties").keys())

    @classmethod
    def getClassFields(cls, by_alias=False) -> list[str]:
        field_names = []
        for key, value in cls.model_fields.items():
            if by_alias and value.alias:
                field_names.append(value.alias)
            else:
                field_names.append(key)

        return field_names

    def __str__(self):
        """Returns the string representation of this object."""
        return self.getClassName()

    def __repr__(self):
        """Returns the string representation of this object."""
        return str(self)


class AbstractModel(PydanticAbstractModel):
    """AbstractModel is a base model for all models inherit and provides basic configuration parameters."""

    # auditable properties
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @model_validator(mode="before")
    @classmethod
    def preValidator(cls, values: Any) -> Any:
        """Before validators: are run before the model is instantiated. These are more flexible than after validators,
        but they also have to deal with the raw input, which in theory could be any arbitrary object.

        Note:- The order of annotations should be same as given here to invoke it automatically.
            @model_validator(mode="before")
            @classmethod
        """
        logger.debug(f"+preValidator(), values={values}")
        # <class 'pydantic._internal._model_construction.ModelMetaclass'>
        # if isinstance(values, dict):
        #     if 'created_at' in values:
        #         raise ValueError("'created_at' should not be included!")
        #     if 'updated_at' in values:
        #         raise ValueError("'updated_at' should not be included!")

        logger.debug(f"-preValidator(), values={values}")
        return values

    @model_validator(mode="after")
    def postValidator(self, values) -> Self:
        """After validators: run after the whole model has been validated. As such, they are defined as instance methods
        and can be seen as post-initialization hooks. Important note: the validated instance should be returned.
        """
        logger.debug(f"postValidator() => type={type(self)}, values={values}")
        return self

    # @model_validator(mode="wrap")
    # def modelValidator(self, values) -> Self:
    #     """Wrap validators: are the most flexible of all. You can run code before or after Pydantic and other validators
    #     process the input data, or you can terminate validation immediately, either by returning the data early or by
    #     raising an error.
    #     """
    #     logger.debug(f"modelValidator() => type={type(self)}, values={values}")
    #     return self

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{self.getClassName()} => type={type(self)}, object={str(self)}")
        return self.model_dump_json()

    def toJSONObject(self) -> Any:
        # return {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}
        logger.debug(
            f"{self.getClassName()} => type={type(self)}, object={str(self)}, json={self.model_dump(mode='json')}")
        return self.model_dump(mode="json")

    def _auditable(self) -> str:
        """Returns the string representation of this object"""
        return f"created_at={self.created_at}, updated_at={self.updated_at}"

    @classmethod
    def validate_and_raise(cls, data, is_query_params: bool = False):
        try:
            if is_query_params:
                for k, v in data.items():
                    if ',' in v:
                        data[k] = v.split(',')
            return cls(**data)

        except ValidationError as e:
            # later can use the error response class and throw 422 validation error
            logger.error(f"Failed to validate [{type(cls)}]! Error={e}")
            for it in e.errors():
                logger.error(f"it={it}")

            raise e

    @classmethod
    def listOfClassInstances(cls, data: List[Dict]) -> List['AbstractModel']:
        """Converts a list of dictionaries into a list of class instances.

        Arguments:
            - data: A list of dictionaries, each representing an instance of the model.

        Returns:
            A list of validated class instances.
        """
        return list(map(lambda it: cls(**it), data))

    @classmethod
    def toResponse(cls, data: Union['AbstractModel', List['AbstractModel']]) -> Union[None, List[Dict], Dict]:
        """Converts an instance or list of instances of the pydantic classes into a serializable format.

        Arguments:
            - data: A single class instance or a list of class instances.

        Returns:
            A dictionary or list of dictionaries representing the data, or None if no data is provided.
        """
        if isinstance(data, list):
            # Use `dict()` instead of `model_dump()` for better compatibility
            return list(map(lambda it: it.dict(), data))
        elif isinstance(data, cls):
            return data.model_dump()

        return None


class BaseModel(AbstractModel):
    """BaseModel is a base model for all models inherit and provides basic configuration parameters."""

    id: int | None = None

    # @root_validator()
    # def on_create(cls, values):
    #     logger.debug(f"on_create({values})")
    #     print("Put your logic here!")
    #     return values

    @model_validator(mode="before")
    @classmethod
    def preValidator(cls, values: Any) -> Any:
        """Before validators: are run before the model is instantiated. These are more flexible than after validators,
        but they also have to deal with the raw input, which in theory could be any arbitrary object.

        Note:- The order of annotations should be same as given here to invoke it automatically.
            @model_validator(mode="before")
            @classmethod
        """
        logger.debug(f"+preValidator(), type={type(values)} values={values}")
        # <class 'pydantic._internal._model_construction.ModelMetaclass'>
        if not isinstance(values, dict):
            raise ValueError("Invalid 'Model' type!")

        if isinstance(values, dict):
            if not values:
                raise ValueError("'Model' is not fully defined!")

        #     if 'created_at' in values:
        #         raise ValueError("'created_at' should not be included!")
        #     if 'updated_at' in values:
        #         raise ValueError("'updated_at' should not be included!")

        logger.debug(f"-preValidator(), values={values}")
        return values

    @model_validator(mode="after")
    def postValidator(self, values) -> Self:
        """After validators: run after the whole model has been validated. As such, they are defined as instance methods
        and can be seen as post-initialization hooks. Important note: the validated instance should be returned.
        """
        logger.debug(f"postValidator() => type={type(self)}, values={values}")
        return self

    def get_id(self):
        return self.id

    def load_and_not_raise(self, data):
        try:
            return self.load(data)
        except ValidationError as ex:
            logger.error(f"load_and_not_raise() => Error:{ex.errors()}")
            # err = get_error(exception=None, msg=e.messages, status=422)
            # return abort(make_response(err, err.get('error').get('status')))

    def validate_and_raise(self, data):
        errors = self.model_validate(data)
        if errors:
            logger.error(f"validate_and_raise() => Error:{errors}")
            # err = get_error(exception=None, msg=errors, status=422)
            # return abort(make_response(err, err.get('error').get('status')))

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{self.getClassName()} <id={self.get_id()}, {self._auditable()}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class NamedModel(BaseModel):
    """NamedModel used an entity with a property called 'name' in it"""

    name: str

    @model_validator(mode="before")
    @classmethod
    def preValidator(cls, values: Any) -> Any:
        logger.debug(f"+preValidator(), values={values}")
        # logging.error(f"Model [{cls}] failed to validate values={values}!")
        superPreValidated = super().preValidator(values)
        if isinstance(values, dict):
            if "name" not in values:
                raise ValueError("The model 'name' should be provided!")

        logger.debug(f"-preValidator(), values={values}")
        return values

    @field_validator('name')
    @classmethod
    def nameValidator(cls, value: str):
        logger.info(f"nameValidator({value})")
        if value is None or len(value.strip()) == 0:
            raise ValueError("The model 'name' should not be null or empty!")

        return value

    def get_name(self):
        return self.name

    def __str__(self):
        """Returns the string representation of this object"""
        return f"{self.getClassName()} <id={self.get_id()}, name={self.get_name()}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class ErrorModel(AbstractModel):
    """ErrorModel represents the error object"""
    status: int = None
    message: str = None
    debug_info: Optional[Dict[str, object]] = None

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{self.getClassName()} => type={type(self)}, object={str(self)}")
        return self.model_dump_json(exclude=["created_at", "updated_at"])

    @staticmethod
    def buildError(httpStatus: HTTPStatus, message: str = None, exception: Exception = None,
                   is_critical: bool = False):
        """
        Builds the error object for the provided arguments
        Parameters:
            httpStatus: status of the request
            message: message of the error
            exception: exception for the error message
            is_critical: is error a critical error
        """
        logger.debug(f"buildError({httpStatus}, {message}, {exception}, {is_critical})")

        # set message, if missing
        if message is None:
            if exception is not None:
                message = str(exception)
            elif httpStatus:
                message = httpStatus.message

        # debug details
        debug_info = {}
        if is_critical and exception is not None:
            debug_info['exception'] = Utils.stackTrace(exception)
            return ErrorModel(status=httpStatus.statusCode, message=message, debug_info=debug_info)
        elif exception is not None:
            debug_info['exception'] = Utils.stackTrace(exception)
            return ErrorModel(status=httpStatus.statusCode, message=message, debug_info=debug_info)
        else:
            return ErrorModel(status=httpStatus.statusCode, message=message)

    @classmethod
    def jsonResponse(cls, httpStatus: HTTPStatus, message: str = None, exception: Exception = None,
                     is_critical: bool = False):
        return ErrorModel.buildError(httpStatus, message, exception, is_critical).to_json()

    def __str__(self):
        """Returns the string representation of this object"""
        return f"{self.getClassName()} <status={self.status}, message={self.message}, debug_info={self.debug_info}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class ResponseModel(AbstractModel):
    """ResponseModel represents the response object"""
    status: int
    message: Optional[str] = None
    data: Optional[List[BaseModel]] = None
    errors: Optional[List[ErrorModel]] = None

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{self.getClassName()} => type={type(self)}, object={str(self)}")
        jsonObjects = {field: getattr(self, field) for field in self.getAllFields()}
        jsonObjects.pop("created_at")
        jsonObjects.pop("updated_at")
        # logger.debug(f"jsonObjects type={type(jsonObjects)}, jsonObjects={jsonObjects}")
        # parse list of data to json
        if jsonObjects['data']:
            jsonData = []
            for item in jsonObjects['data']:
                # logger.debug(f"entry type={type(item)}, item={item}, json={item.to_json()}")
                jsonData.append(json.loads(item.to_json()))

            jsonObjects['data'] = jsonData

        # parse list of errors to json
        if jsonObjects['errors']:
            jsonErrors = []
            for item in jsonObjects['errors']:
                # logger.debug(f"entry type={type(item)}, item={item}, json={item.to_json()}")
                jsonErrors.append(json.loads(item.to_json()))

            jsonObjects['errors'] = jsonErrors

        return jsonObjects

    def toJSONObject(self) -> Any:
        # return {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}
        # return self.model_dump(mode="json", serialize_as_any=True)
        # return self.model_dump(mode="json")
        jsonObject = self.model_dump(mode="json")
        for entry in self.data:
            logger.debug(f"entry type={type(entry)}, object={entry}")

        jsonObject["data"] = self.data.model_dump(mode="json")
        jsonObject["errors"] = self.errors.model_dump(mode="json")

        return jsonObject

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{self.getClassName()} <status={self.status}, data={self.data}, errors={self.errors}>"

    def addInstance(self, instance: AbstractModel = None):
        """Adds an object into the list of data or errors"""
        logger.debug(
            f"+addInstance({instance}) => type={type(instance)}, object={str(instance)}, json={instance.to_json()}")
        if isinstance(instance, ErrorModel):
            if self.errors is None and instance:
                self.errors = []

            self.errors.append(instance)

        elif isinstance(instance, BaseModel):
            if self.data is None and instance:
                self.data = []

            self.data.append(instance)
        else:
            logger.debug(f"Invalid instance:{instance}!")

        logger.debug(f"-addInstance(), data={self.data}, errors={self.errors}, json={self.to_json()}")

    def addInstances(self, instances: List[AbstractModel] = None):
        logger.debug(f"+addInstances(), instances={instances}")
        for instance in instances:
            self.addInstance(instance)

        logger.debug(f"-addInstances()")

    def hasError(self) -> bool:
        """Returns true if any errors otherwise false"""
        return self.errors is not None

    @classmethod
    def buildResponse(cls, httpStatus: HTTPStatus, instance: AbstractModel = None, message: str = None,
                      exception: Exception = None, is_critical: bool = False):
        logger.debug(f"+buildResponse({httpStatus}, {instance}, {message}, {exception}, {is_critical})")
        if isinstance(instance, ErrorModel):  # check if an ErrorModel entity
            logger.debug(f"isinstance(entity, ErrorModel) => {isinstance(instance, ErrorModel)}")
            errorModel = ErrorModel.buildError(httpStatus, message, exception, is_critical)
            # update entity's message and exception if missing
            if not errorModel.message:
                errorModel.message = instance.message if instance.message else errorModel.message

            # build response and add errorModel in the list
            response = ResponseModel(status=httpStatus.statusCode)
            response.addInstance(errorModel)
        elif isinstance(instance, BaseModel):
            logger.debug(f"isinstance(entity, AbstractModel) => {isinstance(instance, BaseModel)}")
            response = ResponseModel(status=httpStatus.statusCode)
            # build errorModel response, if exception is provided
            if HTTPStatus.isStatusSuccess(httpStatus):
                # if not exception or not message:
                response.addInstance(instance)
            else:
                response.addInstance(ErrorModel.buildError(httpStatus, message, exception, is_critical))
        elif exception:
            logger.debug(f"elif exception => type={type(exception)}, exception={exception}")
            response = ResponseModel(status=httpStatus.statusCode)
            # build errorModel response, if exception is provided
            response.addInstance(ErrorModel.buildError(httpStatus, message, exception, is_critical))
        elif not HTTPStatus.isStatusSuccess(httpStatus):
            logger.debug(f"not HTTPStatus.isStatusSuccess() => {HTTPStatus.isStatusSuccess(httpStatus)}")
            response = ResponseModel(status=httpStatus.statusCode)
            # build errorModel response, if exception is provided
            response.addInstance(ErrorModel.buildError(httpStatus, message, exception, is_critical))
        else:
            logger.debug(f"else => ")
            response = ResponseModel(status=httpStatus.statusCode)

        logger.debug(f"-buildResponse(), response={response}")
        return response

    @classmethod
    def buildResponseWithException(cls, exception: AbstractException):
        logger.debug(f"+buildResponseWithException() => type={type(exception)}")
        # build response and add errorModel in the list
        if isinstance(exception, ValidationException):  # check if an AbstractException entity
            logger.debug(f"ValidationException => {isinstance(exception, ValidationException)}")
            response = ResponseModel(status=exception.httpStatus.statusCode)
            for message in exception.messages:
                response.addInstance(ErrorModel.buildError(httpStatus=exception.httpStatus, message=message))
        elif isinstance(exception, DuplicateRecordException):
            logger.debug(f"DuplicateRecordException => {isinstance(exception, DuplicateRecordException)}")
            response = ResponseModel(status=exception.httpStatus.statusCode)
            response.addInstance(
                ErrorModel.buildError(httpStatus=exception.httpStatus, message=exception.messages[:-1]))
        elif isinstance(exception, NoRecordFoundException):
            logger.debug(f"NoRecordFoundException => {isinstance(exception, NoRecordFoundException)}")
            response = ResponseModel(status=exception.httpStatus.statusCode)
            response.addInstance(
                ErrorModel.buildError(httpStatus=exception.httpStatus, message=exception.messages[:-1])
            )
            # response = ResponseModel.buildResponse(HTTPStatus.CONFLICT, message=str(exception))
        elif isinstance(exception, AbstractException):
            logger.debug(f"isinstance(exception, AbstractException) => {isinstance(exception, AbstractException)}")
            response = ResponseModel(status=exception.httpStatus.statusCode)
            for message in exception.messages:
                response.addInstance(ErrorModel.buildError(httpStatus=exception.httpStatus, message=message))

            response = ResponseModel.buildResponse(HTTPStatus.CONFLICT, message=str(exception))
        elif isinstance(exception, Exception):
            logger.debug(f"isinstance(exception, Exception) => {isinstance(exception, Exception)}")
            response = ResponseModel(status=HTTPStatus.INTERNAL_SERVER_ERROR)
            # build errorModel response, if exception is provided
            response.addInstance(ErrorModel.buildError(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(exception)))

        logger.debug(f"-buildResponseWithException(), type={type(exception)} response={response}")
        return response

    @classmethod
    def jsonResponseWithException(cls, exception: AbstractException):
        logger.debug(f"+jsonResponseWithException({exception})")
        response = cls.buildResponseWithException(exception).to_json()
        logger.debug(f"-jsonResponseWithException(), response={response}")
        return response

    @classmethod
    def jsonResponse(cls, httpStatus: HTTPStatus, instance: AbstractModel = None, message: str = None,
                     exception: Exception = None, is_critical: bool = False):
        return ResponseModel.buildResponse(httpStatus, instance, message, exception, is_critical).to_json()

    @classmethod
    def jsonResponses(cls, httpStatus: HTTPStatus, instances: Optional[List[AbstractModel]] = []):
        logger.debug(f"jsonResponses() => httpStatus={httpStatus}")
        response = ResponseModel.buildResponse(httpStatus=httpStatus)
        for instance in instances:
            response.addInstance(instance)

        return response.to_json()
