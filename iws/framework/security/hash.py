#
# Author: Rohtash Lakra
#

import hashlib
import logging

from framework.enums import BaseEnum
from framework.utils import Utils

logger = logging.getLogger(__name__)

UTF_8 = "utf-8"


class HashUtils(BaseEnum):

    @classmethod
    def hashDigestAndBase64(cls, text: str):
        logger.debug(f"+hashDigestAndBase64({text})")
        hashEncoded = hashlib.sha256(text.encode())
        hashDigest = hashEncoded.digest()
        hashBase64 = hashDigest.hex()
        logger.debug(f"-hashDigestAndBase64(), hashDigest={hashDigest}, hashBase64={hashBase64}")
        return hashDigest, hashBase64

    @classmethod
    def hashCode(cls, text):
        hashDigest, hashBase64 = cls.hashDigestAndBase64(text)
        return hashBase64

    @classmethod
    def hashCodeWithSalt(cls, textHashCode, salt: str = Utils.randomUUID()):
        # salt = Utils.randomUUID()
        # saltBytes = bytes(salt, UTF_8)
        saltBytes = salt.encode()
        saltEncoded = hashlib.sha256(saltBytes)
        saltDigest = saltEncoded.digest()
        saltBase64 = saltBytes.hex()

        hashBase64 = textHashCode + saltDigest.hex()

        return saltBase64, hashBase64

    @classmethod
    def checkHashCode(cls, text, salt, hash) -> bool:
        # logger.debug(f"+checkHashCode({text}, {salt}, {hash})")
        saltBytes = bytes.fromhex(salt)
        hashBytes = bytes.fromhex(hash)

        saltSHA256Object = hashlib.sha256(saltBytes)
        saltDigest = saltSHA256Object.digest()
        textSHA256Object = hashlib.sha256(text.encode())
        textDigest = textSHA256Object.digest()

        authenticated = (textDigest + saltDigest) == hashBytes
        # logger.debug(f"-checkHashCode(), authenticated={authenticated}")
        logger.debug(f"checkHashCode(), authenticated={authenticated}")
        return authenticated
