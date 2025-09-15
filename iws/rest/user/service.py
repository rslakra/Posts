#
# Author: Rohtash Lakra
#
import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from common.config import Config
from framework.exception import (
    DuplicateRecordException,
    ValidationException,
    RecordNotFoundException,
    AuthenticationException
)
from framework.http import HTTPStatus
from framework.orm.pydantic.model import BaseModel
from framework.orm.sqlalchemy.schema import SchemaOperation
from framework.security.crypto import CryptoUtils
from framework.security.crypto import SecurityException
from framework.security.hash import HashUtils
from framework.security.jwt import AuthModel, AuthenticatedUser, TokenTypeEnum
from framework.service import AbstractService
from framework.utils import Utils
from rest.user.mapper import UserMapper
from rest.user.model import User, LoginUser
from rest.user.repository import UserRepository, UserSecurityRepository
from rest.user.schema import UserSecuritySchema

logger = logging.getLogger(__name__)


class UserService(AbstractService):
    
    def __init__(self):
        logger.debug(f"UserService()")
        self.userRepository = UserRepository()
        self.userSecurityRepository = UserSecurityRepository()
    
    def validate(self, operation: SchemaOperation, user: User) -> None:
        logger.debug(f"+validate({operation}, {user})")
        # super().validate(operation, user)
        error_messages = []
        
        # validate the object
        if user:
            match operation.name:
                case SchemaOperation.CREATE.name:
                    # validate the required fields
                    if not user.email:
                        error_messages.append("User 'email' is required!")
                    
                    if not user.first_name:
                        error_messages.append("User 'first_name' is required!")
                    
                    if not user.last_name:
                        error_messages.append("User 'last_name' is required!")
                    
                    if not user.birth_date:
                        error_messages.append("User 'birth_date' is required!")
                    
                    if not user.user_name:
                        error_messages.append("User 'user_name' is required!")
                    
                    if not user.password:
                        error_messages.append("User 'password' is required!")
                
                case SchemaOperation.UPDATE.name:
                    if not user.id:
                        error_messages.append("User 'id' is required!")
        else:
            error_messages.append("'User' is not fully defined!")
        
        # throw an error if any validation error
        logger.debug(f"error_messages={error_messages}")
        if error_messages and len(error_messages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=error_messages)
            logger.debug(f"-validate(), {type(error)} = exception={error}")
            raise error
        
        logger.debug(f"-validate()")
    
    # @override
    def findByFilter(self, filters: Dict[str, Any]) -> List[Optional[BaseModel]]:
        """Returns the records based on the provided filters"""
        logger.debug(f"+findByFilter({filters})")
        schemaObjects = self.userRepository.filter(filters)
        modelObjects = [UserMapper.fromSchema(schemaObject) for schemaObject in schemaObjects]
        logger.debug(f"-findByFilter(), modelObjects={modelObjects}")
        return modelObjects
    
    # @override
    def existsByFilter(self, filters: Dict[str, Any]) -> bool:
        """Returns True if the records exist by filter otherwise False"""
        logger.debug(f"+existsByFilter({filters})")
        schemaObjects = self.userRepository.filter(filters)
        result = True if schemaObjects else False
        logger.debug(f"-existsByFilter(), result={result}")
        return result
    
    def validates(self, operation: SchemaOperation, users: List[User]) -> None:
        """Validates the objects based on the operation"""
        logger.debug(f"+validates({operation}, {users})")
        error_messages = []
        
        # validate the object
        if not users:
            error_messages.append('Users is required!')
        
        for user in users:
            self.validate(operation, user)
        
        # throw an error if any validation error
        if error_messages and len(error_messages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=error_messages)
            logger.debug(f"{type(error)} = exception={error}")
            raise error
        
        logger.debug(f"-validates()")
    
    def register(self, modelObject: User) -> User:
        """Crates/Registers a new user"""
        logger.debug(f"+register({modelObject})")
        self.validate(SchemaOperation.CREATE, modelObject)
        # check user already exists or not
        if self.existsByFilter({"email": modelObject.email}):
            raise DuplicateRecordException(HTTPStatus.CONFLICT, f"User '{modelObject.email}' is already registered!")
        
        # load user's email address
        # roleService = RoleService()
        # roleModel = roleService.findByFilter({"name": "Owner"})
        # logger.debug(f"roleModel={roleModel}")
        schemaObject = UserMapper.fromModel(modelObject)
        schemaObject = self.userRepository.save(schemaObject)
        
        # persist user's security
        passwordHashCode = HashUtils.hashCode(modelObject.password)
        logger.debug(f"modelObject.password={modelObject.password}, passwordHashCode={passwordHashCode}")
        # saltHashCode, hashCode = HashUtils.hashCodeWithSalt(passwordHashCode)
        # logger.debug(f"saltHashCode={saltHashCode}, hashCode={hashCode}")
        # TODO: Capture platform value form user-agent
        userSecuritySchema = UserSecuritySchema(platform="Service", salt=Utils.randomUUID(),
                                                hashed_auth_token=passwordHashCode)
        logger.debug(f"userSecuritySchema={userSecuritySchema}")
        schemaObject.user_security = userSecuritySchema
        userSecuritySchema = self.userRepository.save(userSecuritySchema)
        logger.debug(f"userSecuritySchema={userSecuritySchema}")
        
        modelObject = UserMapper.fromSchema(schemaObject)
        logger.debug(f"modelObject={modelObject}")
        # user = User.model_validate(userSchema)
        
        # # build auth-token
        # authModel = AuthModel(user_id=modelObject.id, auth_token=modelObject.password,
        #                       iat=int(datetime.now(timezone.utc).timestamp()))
        # authModelEncrypted = CryptoUtils.encrypt_with_aesgcm(Config.ENC_KEY, Config.ENC_NONCE, authModel.to_json())
        # logger.debug(f"authModelEncrypted={authModelEncrypted}")
        
        logger.debug(f"-register(), modelObject={modelObject}")
        return modelObject
    
    def bulkCreate(self, users: List[User]) -> List[User]:
        """Crates users in bulk"""
        logger.debug(f"+bulkCreate({users})")
        results = []
        for user in users:
            result = self.register(user)
            results.append(result)
        
        logger.debug(f"-bulkCreate(), results={results}")
        return results
    
    def authenticate(self, token_type: TokenTypeEnum, auth_token: str) -> User:
        """Authenticates the token"""
        logger.debug(f"+authenticate({token_type}, {auth_token})")
        try:
            # JWT Based Authentication
            if TokenTypeEnum.JWT == TokenTypeEnum:
                raise AuthenticationException(HTTPStatus.UNAUTHORIZED, "Not yet supported!")
            else:
                try:
                    authModelDecrypted = CryptoUtils.decrypt_with_aesgcm(Config.ENC_KEY, Config.ENC_NONCE, auth_token)
                except SecurityException as ex:
                    raise AuthenticationException(HTTPStatus.INTERNAL_SERVER_ERROR, messages=[str(ex)])
                
                logger.debug(f"type={type(authModelDecrypted)}, authModelDecrypted={authModelDecrypted}")
                authModel = AuthModel(**authModelDecrypted)
                
                # TODO: Time comparison with iat and expiry max
                userSecuritySchema = self.userSecurityRepository.filter({"user_id": authModel.user_id})[0]
                if userSecuritySchema:
                    passwordHashCode = HashUtils.hashCode(authModel.auth_token)
                    if userSecuritySchema.hashed_auth_token != passwordHashCode:
                        raise AuthenticationException(HTTPStatus.UNAUTHORIZED, "Invalid Token!")
                    
                    if userSecuritySchema.expire_at and userSecuritySchema.expire_at < int(
                            datetime.now(timezone.utc).timestamp()):
                        raise AuthenticationException(HTTPStatus.UNAUTHORIZED, "Auth token has expired!")
                    
                    saltHashCode, hashCode = HashUtils.hashCodeWithSalt(passwordHashCode, userSecuritySchema.salt)
                    if not HashUtils.checkHashCode(authModel.auth_token, saltHashCode, hashCode):
                        raise AuthenticationException(HTTPStatus.UNAUTHORIZED, "Invalid Token!")
                    
                    # load authenticated user
                    schemaObject = self.userRepository.filter({"id": authModel.user_id})[0]
                    userObject = UserMapper.fromSchema(schemaObject)
                    userObject.authenticated = True
        
        except Exception as e:
            logger.error(f"Auth token {auth_token} seems to have been tampered!, Error:{e}")
            raise AuthenticationException(HTTPStatus.UNAUTHORIZED, str(e))
        
        logger.debug(f"-authenticate(), userObject={userObject}")
        return userObject
    
    def login(self, loginUser: LoginUser) -> AuthenticatedUser:
        """Login a registered user"""
        logger.debug(f"+{self.__class__.__name__}.login({loginUser})")
        # validate login-info
        error_messages = []
        
        # validate either an email or user_name is provided
        if not (loginUser and (Utils.is_valid_email(loginUser.email) or Utils.is_valid_username(loginUser.user_name))):
            error_messages.append("Either email or user_name is required!")
        
        # throw an error if any validation error
        if error_messages and len(error_messages) > 0:
            logger.error(f"error_messages={error_messages}")
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=error_messages)
            logger.debug(f"-validate(), {type(error)} = exception={error}")
            raise error
        
        userObjects = None
        # load user either by email or user_name
        if loginUser.email:
            userObjects = self.findByFilter({"email": loginUser.email})
        elif loginUser.user_name:
            userObjects = self.findByFilter({"user_name": loginUser.user_name})
        
        # validate user exists either by email or username
        if not (userObjects and len(userObjects) > 0):
            raise RecordNotFoundException(HTTPStatus.NOT_FOUND, messages=["User is not registered!"])
        
        # authenticate user by loading user's credentials
        userObject = userObjects[0]
        userSecuritySchema = self.userSecurityRepository.filter({"user_id": userObject.id})[0]
        logger.debug(f"userSecuritySchema={userSecuritySchema}")
        
        # validate password
        passwordHashCode = HashUtils.hashCode(loginUser.password)
        logger.debug(f"loginUser.password={loginUser.password}, passwordHashCode={passwordHashCode}")
        # check the hashed-auth-token and password-auth-token are same
        if userSecuritySchema.hashed_auth_token != passwordHashCode:
            raise AuthenticationException(HTTPStatus.UNAUTHORIZED, messages=["Either username or password is wrong!"])
        
        # check other patterns
        saltHashCode, hashCode = HashUtils.hashCodeWithSalt(passwordHashCode, userSecuritySchema.salt)
        userObject.authenticated = HashUtils.checkHashCode(loginUser.password, saltHashCode, hashCode)
        logger.debug(f"userObject={userObject}")
        if not userObject.isAuthenticated():
            raise AuthenticationException(HTTPStatus.UNAUTHORIZED, messages=["Either username or password is wrong!"])
        
        # build auth-token model
        authModel = AuthModel(user_id=userObject.id,
                              auth_token=loginUser.password,
                              iat=int(datetime.now(timezone.utc).timestamp()))
        
        # encrypt authModel for security purpose
        try:
            authModelEncrypted = CryptoUtils.encrypt_with_aesgcm(Config.ENC_KEY, Config.ENC_NONCE, authModel.to_json())
        except SecurityException as ex:
            raise AuthenticationException(HTTPStatus.INTERNAL_SERVER_ERROR, messages=[str(ex)])
        
        logger.debug(f"authModelEncrypted={authModelEncrypted}")
        # build authenticate user object model
        authUser = AuthenticatedUser(user_id=authModel.user_id,
                                     token_type=TokenTypeEnum.AUTH.value,
                                     token=authModelEncrypted,
                                     user_exists=True)
        
        logger.debug(f"-{self.__class__.__name__}.login(), authUser={authUser}")
        return authUser
    
    def update(self, user: User) -> User:
        """Updates the user"""
        logger.debug(f"+update({user})")
        # self.validate(SchemaOperation.UPDATE, user)
        # check record exists by id
        if not self.existsByFilter({"id": user.id}):
            raise RecordNotFoundException(HTTPStatus.NOT_FOUND, f"User doesn't exist!")
        
        userSchemas = self.userRepository.filter({"id": user.id})
        userSchema = userSchemas[0]
        #  Person
        if user.email and userSchema.email != user.email:
            userSchema.email = user.email
        if user.first_name and userSchema.first_name != user.first_name:
            userSchema.first_name = user.first_name
        if user.last_name and userSchema.last_name != user.last_name:
            userSchema.last_name = user.last_name
        if user.birth_date and userSchema.birth_date != user.birth_date:
            userSchema.birth_date = user.birth_date
        #  User
        if user.user_name and userSchema.user_name != user.user_name:
            userSchema.user_name = user.user_name
        if user.admin and userSchema.admin != user.admin:
            userSchema.admin = user.admin
        if user.last_seen and userSchema.last_seen != user.last_seen:
            userSchema.last_seen = user.last_seen
        if user.avatar_url and userSchema.avatar_url != user.avatar_url:
            userSchema.avatar_url = user.avatar_url
        
        # userSchema = CompanyMapper.fromModel(oldRole)
        self.userRepository.update(userSchema)
        # userSchema = self.userRepository.update(mapper=UserSchema, mappings=[userSchema])
        userSchema = self.userRepository.filter({"id": user.id})[0]
        user = UserMapper.fromSchema(userSchema)
        logger.debug(f"-update(), user={user}")
        return user
    
    def delete(self, id: int) -> None:
        logger.debug(f"+delete({id})")
        # check record exists by id
        filter = {"id": id}
        if self.existsByFilter(filter):
            self.userRepository.delete(filter)
        else:
            raise RecordNotFoundException(HTTPStatus.NOT_FOUND, "User doesn't exist!")
        
        logger.debug(f"-delete()")
