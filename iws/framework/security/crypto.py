#
# Author: Rohtash Lakra
#

import base64
import json
import logging
import secrets
import string

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

logger = logging.getLogger(__name__)

UTF_8 = 'utf-8'


class SecurityException(Exception):
    """ Security Exception """
    pass


class CryptoUtils:
    """"""

    extra_data = None

    # @staticmethod
    # @property
    # def extra_data():
    #     return CryptoUtils._extra_data
    #
    # @staticmethod
    # @extra_data.setter
    # def extra_data(value):
    #     CryptoUtils._extra_data = value

    @staticmethod
    def nonce_token(length: int):
        """Generates a random nonce token of the provided length."""
        logger.debug(f"+nonce_token({length})")
        # Use digits only
        # characters = string.digits
        # Use both lowercase and uppercase letters (string.ascii_letters) as well as digits (string.digits).
        alpha_numeric = string.ascii_letters + string.digits
        # Generate the token
        token = ''.join(secrets.choice(alpha_numeric) for _ in range(length))

        logger.debug(f"-nonce_token(), token={token}")
        return token

    @staticmethod
    def encrypt_with_aesgcm(enc_key: str, enc_nonce: str, data: str) -> str:
        logger.debug(f"+encrypt_with_aesgcm({enc_key}, {enc_nonce}, {data})")
        if not (enc_key or enc_nonce):
            raise SecurityException("Either security key or nonce is wrong!")

        aesgcm = AESGCM(enc_key.encode(UTF_8))
        data_bytes = aesgcm.encrypt(enc_nonce.encode(UTF_8), data.encode(UTF_8), CryptoUtils.extra_data)
        encrypted = base64.b64encode(data_bytes).decode(UTF_8)
        logger.debug(f"-encrypt_with_aesgcm(), encrypted={encrypted}")
        return encrypted

    @staticmethod
    def decrypt_with_aesgcm(enc_key: str, enc_nonce: str, data: str) -> dict:
        logger.debug(f"+decrypt_with_aesgcm({enc_key}, {enc_nonce}, {data})")
        if not (enc_key or enc_nonce):
            raise SecurityException("Either security key or nonce is wrong!")

        aesgcm = AESGCM(enc_key.encode(UTF_8))
        data_bytes = base64.b64decode(data)
        decrypted = aesgcm.decrypt(enc_nonce.encode(UTF_8), data_bytes, CryptoUtils.extra_data).decode(UTF_8)
        decrypted = json.loads(decrypted)
        logger.debug(f"-decrypt_with_aesgcm(), type={type(decrypted)}, decrypted={decrypted}")
        return decrypted

    @staticmethod
    def random_password(length: int = 10, atLeastDigits: int = 1) -> str:
        """
        Generate a ten-character alphanumeric password with at least one lowercase character, at least one uppercase character, and at least three digits:
        """
        alphabet = string.ascii_letters + string.digits
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(length))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password) >= atLeastDigits):
                break

        return password
