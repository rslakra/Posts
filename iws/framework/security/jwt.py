#
# Author: Rohtash Lakra
# Reference:
# - https://pyjwt.readthedocs.io/en/2.10.1/
#
import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from enum import auto, unique
from typing import Union, Optional, Any, Dict

import jwt
import requests
from lib2to3.btm_utils import tokens

from framework.enums import BaseEnum
from framework.exception import AuthenticationException, ValidationException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import AbstractModel, BaseModel

logger = logging.getLogger(__name__)


@unique
class JwtAlgoEnum(BaseEnum):
    """TokenTypeEnum Enum. For readability, add constants in Alphabetical order."""
    HS256 = auto()


@unique
class JWTEnum(BaseEnum):
    """TokenTypeEnum Enum. For readability, add constants in Alphabetical order."""
    AUDIENCE = 'aud'
    ISSUER = 'iss'
    ISSUED_AT = 'iat'
    EXPIRY = 'exp'
    SUBJECT = 'sub'
    TYPE = 'type'
    GRANT_TYPE = 'grant_type'
    CLIENT_ID = 'client_id'
    CLIENT_SECRET = 'clientSecret'
    DEFAULT_ISSUER = 'RSLakra'


@unique
class TokenTypeEnum(BaseEnum):
    """TokenTypeEnum Enum. For readability, add constants in Alphabetical order."""
    AUTH = "Password"
    JWT = "jwt"
    OAUTH = "oauth"
    ACCESS_TOKEN = 'access_token'
    REFRESH_TOKEN = 'refresh_token'
    
    @classmethod
    def isAccessToken(cls, token: Dict[str, Any]) -> bool:
        return token and TokenTypeEnum.ACCESS_TOKEN.value == token[JWTEnum.TYPE.value]
    
    @classmethod
    def isRefreshToken(cls, token: Dict[str, Any]) -> bool:
        return token and TokenTypeEnum.REFRESH_TOKEN.value == token[JWTEnum.TYPE.value]


class JWTTokenModel(AbstractModel):
    """JWTTokenModel represents """
    jwt_token: str
    # Time since epoch
    exp: float | int


class JWTModel(AbstractModel):
    """JWTModel contains the payload to create a JWT Token"""
    user_id: str | None = None
    medium: str
    phone_number: str | None = None
    country_code: str | None = None
    email: str | None = None


class UserToken(AbstractModel):
    """User's JWT Token Payload"""
    userId: Optional[str] = None
    refreshToken: Optional[str] = None
    accessToken: Optional[str] = None
    expiresAt: Optional[int] = None


@dataclass(frozen=True)
class TokenPayload:
    """"""
    aud: str
    iss: str
    iat: int
    exp: int
    sub: str
    email: Optional[str] = None
    type: Optional[str] = None
    
    def __str__(self):
        """Converts the dataclass instance to a string."""
        # field_strings = [f"{key}={value}" for key, value in self.__dict__.items()]
        # return f"{self.__class__.__name__} <{', '.join(field_strings)}>"
        return f"{self.__class__.__name__} <{self.as_dict()}>"
    
    def __repr__(self):
        return str(self)
    
    def as_dict(self) -> dict[str, Any]:
        """Generate a dictionary representation of the model."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Converts the dataclass instance to a JSON string."""
        return json.dumps(self.as_dict(), indent=2)  # Using indent for pretty printing
    
    @classmethod
    def equals(cls, decodedToken: dict, jwtField: JWTEnum, expected: Any) -> bool:
        return decodedToken and jwtField and decodedToken[jwtField.value] == expected
    
    @classmethod
    def get_options(cls) -> dict:
        # return {"require": ["aud", "iss", "iat", "exp", "sub", "email", "type"]}
        return {"require": ["aud", "iss", "iat", "exp", "sub"]}


@dataclass(frozen=True)
class RefreshTokenPayload:
    """"""
    client_id: Optional[str]
    client_secret: Optional[str]
    grant_type: Optional[str]
    refresh_token: Optional[str]
    
    def __str__(self):
        """Converts the dataclass instance to a string."""
        # field_strings = [f"{key}={value}" for key, value in self.__dict__.items()]
        # return f"{self.__class__.__name__} <{', '.join(field_strings)}>"
        return f"{self.__class__.__name__} <{self.as_dict()}>"
    
    def __repr__(self):
        return str(self)
    
    def as_dict(self) -> dict[str, Any]:
        """Generate a dictionary representation of the model."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Converts the dataclass instance to a JSON string."""
        return json.dumps(self.as_dict(), indent=2)  # Using indent for pretty printing


class AuthenticatedUser(BaseModel):
    """An Authenticated User's response payload """
    user_id: Union[int | None] = None
    token_type: TokenTypeEnum
    token: str
    user_exists: bool
    # Time since epoch
    exp: Union[float | int | None] = None
    
    def __str__(self) -> str:
        """Returns the string representation of this object"""
        field_strings = [f"{key}={value}" for key, value in self.__dict__.items()]
        return f"{self.getClassName()} <{', '.join(field_strings)}>"


class AuthModel(AbstractModel):
    """Authentication model object."""
    
    user_id: int = None
    auth_token: str = None
    iat: int = None
    
    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        return self.model_dump_json(exclude=["created_at", "updated_at"])
    
    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <user_id={}, auth_token={}, iat={}>"
                .format(self.getClassName(), self.user_id, self.auth_token, self.iat))


class JWTUtils(object):
    ZOOM_VIDEO_SDK_KEY = "ZOOM_VIDEO_SDK_KEY"
    ZOOM_VIDEO_SDK_SECRET = "ZOOM_VIDEO_SDK_SECRET"
    
    @classmethod
    def jwtCreateToken(cls, jwtModel: JWTModel, expiry_in_seconds: int = None,
                       exp: Union[int | float | None] = None) -> JWTTokenModel:
        """Creates a JWT token with the provided params.

        Arguments:
            - jwtModel:(JWTModel): The identity for which the JWT token is being created.
            - expiry_in_hours (int, optional): The number of hours after which the token should expire and defaults to
            24 hours.
            - exp (datetime, optional): The exact expiration time for the token. If provided, this value will be used
            directly. If not provided, it will be calculated based on `expires_in_hours` or the default app
            configuration.

        Returns:
            JWTTokenModel: A Pydantic model contains the JWT token and its expiration time as a Unix timestamp.
        """
        now = datetime.now()
        # the default expiry is 24 hours
        expiry_delta = expiry_in_seconds if expiry_in_seconds else (60 * 60 * 24)
        exp = (now + expiry_delta).timestamp() if exp is None else exp - now
        jwtToken = jwt.encode({"identity": jwtModel.model_dump(),
                               "expiry_delta": expiry_delta
                               },
                              "secret",
                              algorithm=JwtAlgoEnum.HS256.name)
        
        return JWTTokenModel(jwt_token=jwtToken, exp=exp)
    
    @classmethod
    def getIdentity(cls, jwtToken: Union[str | None]):
        """Validates the request contains the JWT token."""
        if jwtToken is None:
            raise AuthenticationException(HTTPStatus.BAD_REQUEST, "The JWT Token must provide in request!")
        
        try:
            # Decode the JWT token
            decodedToken = jwt.decode(jwtToken, "secret", algorithms=[JwtAlgoEnum.HS256.name])
            return decodedToken.get('sub')
        except Exception:
            raise AuthenticationException(HTTPStatus.UNAUTHORIZED, "Invalid or Expired JWT Token!")


class TokenManager:
    """Token Manager handles the token generation and renewal of it.

    Access tokens are short-lived credentials used to authorize specific actions, while refresh tokens are long-lived
    and used to obtain new access tokens. When an access token expires, a new one can be obtained using the refresh
    token, without requiring the user to re-authenticate.

    To handle token expiry in Python, a common approach involves storing the tokens securely and implementing a
    mechanism to check for expiry before making API requests. If the access token has expired, the refresh token is
    used to obtain a new access token and update the stored tokens.
    """
    
    def __init__(self, clientId, clientSecret, expiresInSeconds: int = None, tokenServiceUrl: str = None):
        """Initialize the token manager"""
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.expiresInSeconds = expiresInSeconds
        self.tokenServiceUrl = tokenServiceUrl
        self.tokens: dict[str, UserToken] = dict()
    
    def getIssuedAt(self):
        """Returns current datetime value."""
        return datetime.now(tz=timezone.utc)
    
    def getExpiresInSeconds(self):
        """Return access token expiry - By default, access token expires in 15 (60 * 15) minutes"""
        return self.expiresInSeconds if self.expiresInSeconds else (60 * 15)
    
    def encodeToken(self, tokenPayload: TokenPayload, clientSecret: str,
                    algorithm: str = JwtAlgoEnum.HS256.name) -> str:
        """Encodes the given 'token_payload' using 'clientSecret' and 'algorithm'.
        Args:
            tokenPayload: TokenPayload
            clientSecret: str
            algorithm: JwtAlgoEnum.HS256.name
        """
        logger.debug("+encodeToken(%s, %s, %s)", tokenPayload, clientSecret, algorithm)
        if not tokenPayload:
            raise ValidationException("The 'tokenPayload' should provide.")
        
        if not clientSecret:
            raise ValidationException("The 'clientSecret' should provide.")
        
        encodedToken = jwt.encode(tokenPayload.as_dict(), clientSecret, algorithm=algorithm)
        logger.debug("-encodeToken(%s), encodedToken=%s", tokenPayload, encodedToken)
        return encodedToken
    
    def decodeToken(self,
                    encodedToken: str,
                    clientSecret: str,
                    issuer: str = None,
                    audience: str = None,
                    options: dict = None,
                    algorithm: str = JwtAlgoEnum.HS256.name) -> dict[str, Any]:
        """Decodes the given 'tokenPayload' using 'clientSecret' and 'algorithm'.
        Args:
            encodedToken: str
            clientSecret: str
            issuer: str
            audience: str
            options: dict
            algorithm: JwtAlgoEnum.HS256.name
        """
        # client_secret_hash = HashUtils.md5_hash(clientSecret)
        logger.debug("+decodeToken(%s, %s, %s, %s, %s, %s)", encodedToken, issuer, audience, options, algorithm)
        if not encodedToken:
            raise ValidationException("The 'encodedToken' should provide.")
        
        if not clientSecret:
            raise ValidationException("The 'clientSecret' should provide.")
        
        # decode an access token and validate expiry
        decodedToken = jwt.decode(jwt=encodedToken,
                                  key=clientSecret,
                                  issuer=issuer,
                                  audience=audience,
                                  options=options,
                                  algorithms=algorithm)
        
        logger.debug("-decodeToken(%s), decodedToken=%s", encodedToken, decodedToken)
        return decodedToken
    
    def generateTokens(self, userId: str) -> UserToken:
        """Generates access and refresh tokens for a given user ID."""
        logger.debug(f"+generateTokens({userId}), tokens => {self.tokens}")
        # TODO: Fix ME!
        # if not userId:
        #     err = get_error(exception=None, status=422, msg="The 'user_id' should provide.")
        #     return abort(make_response_extended(err, err.get('error').get('status'), action='rollback'))
        
        # token's issued at
        issuedAt = self.getIssuedAt()
        expiresAt = issuedAt + timedelta(seconds=self.getExpiresInSeconds())
        # access token payload
        accessTokenPayload = TokenPayload(aud=self.clientId,
                                          iss=JWTEnum.DEFAULT_ISSUER.value,
                                          iat=int(issuedAt.timestamp()),
                                          exp=int(expiresAt.timestamp()),
                                          sub=userId,
                                          type=TokenTypeEnum.ACCESS_TOKEN.value)
        logger.debug("accessTokenPayload=%s", accessTokenPayload)
        
        # refresh token payload and expiry - By default, refresh token expires in 30 days
        refreshTokenPayload = TokenPayload(aud=self.clientId,
                                           iss=JWTEnum.DEFAULT_ISSUER.value,
                                           iat=int(issuedAt.timestamp()),
                                           exp=int((issuedAt + timedelta(days=30)).timestamp()),
                                           sub=userId,
                                           type=TokenTypeEnum.REFRESH_TOKEN.value)
        logger.debug("refreshTokenPayload=%s", refreshTokenPayload)
        
        # generate access token
        accessToken = self.encodeToken(accessTokenPayload, self.clientSecret)
        logger.debug("accessToken=%s", accessToken)
        # generate refresh token
        refreshToken = self.encodeToken(refreshTokenPayload, self.clientSecret)
        logger.debug("refreshToken=%s", refreshToken)
        # build user's token and update tokens
        userToken = UserToken(userId=userId, refreshToken=refreshToken, accessToken=accessToken,
                              expiresAt=int(expiresAt.timestamp()))
        # logger.debug(f"userToken={userToken.model_dump(exclude_defaults=True)}")
        logger.debug("userToken=%s", userToken)
        self.tokens[userId] = userToken
        logger.debug("-generateTokens(), userToken=%s, tokens=%s", userToken, self.tokens)
        return userToken
    
    def isExpired(self, expiresAt: int = None) -> bool:
        """Returns true either if expires_at is None or current time >= expires_at, False otherwise"""
        return expiresAt is None or datetime.now().timestamp() >= expiresAt
    
    def refreshAccessToken(self, userId: str, userToken: UserToken = None) -> UserToken:
        """Refreshes an expired access token for the user_id using a valid refresh token."""
        logger.debug("+refreshAccessToken(%s), userToken=%s, tokens=%s", userId, userToken, self.tokens)
        # check a token already exists for the user
        if userId in self.tokens.keys() and not userToken:
            userToken = self.tokens[userId]
            logger.debug("Cached userToken=%s", userToken)
            # validate the existing user's token is not tempered
            if userToken and userToken.userId != userId:
                raise ValidationException('Tempered refresh token!')
        elif not userToken:
            userToken = UserToken(userId=userId)
        
        # check if the token needs to refresh remotely or locally
        if self.tokenServiceUrl:
            # build request's payload
            payload = {
                'grant_type': TokenTypeEnum.REFRESH_TOKEN.value,
                'refresh_token': userToken.refreshToken,
                'client_id': self.clientId,
                'client_secret': self.clientSecret
            }
            
            # send request to refresh token
            response = requests.post(self.tokenServiceUrl, data=payload)
            response.raise_for_status()
            tokenData = response.json()
            # in case of server request, set issued at after getting the response
            issued_at = self.getIssuedAt()
        else:
            # local refresh on the server
            # try:
            logger.debug("Decoding userToken=%s", userToken)
            decodedToken = self.decodeToken(encodedToken=userToken.refreshToken,
                                            clientSecret=self.clientSecret,
                                            issuer=JWTEnum.DEFAULT_ISSUER.value,
                                            audience=self.clientId,
                                            options=TokenPayload.get_options())
            logger.debug("decoded refresh token=%s", decodedToken)
            # validate the token is a type of refresh-token
            if not TokenTypeEnum.isRefreshToken(decodedToken):
                raise ValidationException('Tempered refresh token!')
            # validate the refresh-token is already expired or not
            if self.isExpired(decodedToken[JWTEnum.EXPIRY.value]):
                raise jwt.ExpiredSignatureError('Refresh token is already expired!')
            
            # token's issued at
            issued_at = self.getIssuedAt()
            # access token expiry
            expires_at = issued_at + timedelta(seconds=self.getExpiresInSeconds())
            access_token_payload = TokenPayload(aud=self.clientId,
                                                iss=JWTEnum.DEFAULT_ISSUER.value,
                                                iat=int(issued_at.timestamp()),
                                                exp=int(expires_at.timestamp()),
                                                sub=userId,
                                                type=TokenTypeEnum.ACCESS_TOKEN.value)
            logger.debug(f"access_token_payload={access_token_payload}")
            # new access token using refresh token
            access_token = jwt.encode(access_token_payload.as_dict(), self.clientSecret,
                                      algorithm=JwtAlgoEnum.HS256.name)
            tokenData = {
                TokenTypeEnum.ACCESS_TOKEN.value: access_token
            }
            # except jwt.ExpiredSignatureError:
            #     return "Refresh token has expired. Please log in again."
            # except jwt.InvalidTokenError:
            #     return "Invalid refresh token."
            # except Exception as e:
            #     return str(e)
        
        logger.debug(f"tokenData={tokenData}")
        if tokenData:
            # update user's token object
            userToken.accessToken = tokenData[TokenTypeEnum.ACCESS_TOKEN.value]
            # Some APIs do not return a new refresh token
            userToken.refreshToken = tokenData.get(TokenTypeEnum.REFRESH_TOKEN.value, userToken.refreshToken)
            # If an API doesn't return the token's expiry, set default to 15 minutes
            expiresInSeconds = tokenData.get('expires_in', self.getExpiresInSeconds())
            # access token expiry
            userToken.expiresAt = int((issued_at + timedelta(seconds=expiresInSeconds)).timestamp())
            self.tokens[userId] = userToken
        
        logger.debug(f"-refreshAccessToken(), userToken={userToken}, tokens={self.tokens}")
        return userToken
    
    def getAccessToken(self, user_id: str) -> UserToken:
        """Handles refreshing an access_token on expiry."""
        logger.debug("+getAccessToken(%s), tokens=%s", user_id, self.tokens)
        if user_id in self.tokens.keys():
            userToken = self.tokens[user_id]
            logger.debug("userToken=%s", userToken)
            # validate the token already exists
            if not userToken:
                raise Exception('The provided token is invalid!')
            
            # validate the existing user's token is not tempered
            if userToken.userId != user_id:
                raise Exception('The provided token is either invalid or malformed!')
            
            try:
                # decode an access token and validate expiry
                decodedToken = jwt.decode(userToken.accessToken, self.client_secret,
                                          algorithms=[JwtAlgoEnum.HS256.name])
            except jwt.ExpiredSignatureError as e:
                logger.error(f"Token signature has expired! Error={str(e)}, type={type(e)}")
                userToken = self.refreshAccessToken(user_id)
                userToken.refreshToken = None
            except jwt.InvalidTokenError as e:
                logger.error(f"Error decoding access token! Exception={str(e)}, type={type(e)}")
            else:
                logger.debug("decoded access token=%s", decodedToken)
                if decodedToken:
                    # validate the token is a type of refresh-token
                    if not TokenTypeEnum.isAccessToken(decoded_access_token):
                        raise BadRequestException("The provided token is either invalid or malformed!")
                    
                    # validate if an access-token is expired or not and refresh it
                    if self.isExpired(decodedToken[JWTEnum.EXPIRY.value]):
                        userToken = self.refreshAccessToken(user_id)
                        userToken = copy.copy(userToken)
                        userToken.refreshToken = None
                else:
                    logger.warning("Missing decodedToken!")
        else:
            userToken = self.generateTokens(user_id)
        
        if not userToken:
            raise Exception('Error generating access token!')
        
        logger.debug("-getAccessToken(), userToken=%s", userToken)
        return userToken
