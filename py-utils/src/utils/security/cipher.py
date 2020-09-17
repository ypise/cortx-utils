"""
 ****************************************************************************
 Filename:          cipher.py
 Description:       Wrapper around AES implementation

 Creation Date:     02/11/2019
 Author:            Alexander Voronov

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidSignature, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Cipher:
    """
    Wrapper around actual actual AES implementation (Fernet)

    Serves a single purpose: wraps the actual implementation in order to be able
    to change it in the future.
    """

    @staticmethod
    def encrypt(key: bytes, data: bytes) -> bytes:
        """
        Performs a symmetric encryption of the provided data with the provided key
        """

        return Fernet(key).encrypt(data)

    @staticmethod
    def decrypt(key: bytes, data: bytes) -> bytes:
        """
        Performs a symmetric decryption of the provided data with the provided key
        """

        try:
            decrypted = Fernet(key).decrypt(data)
        except (InvalidSignature, InvalidToken):
            raise CipherInvalidToken(f'Decryption failed')
        return decrypted

    @staticmethod
    def generate_key(str1: str, str2: str, *strs) -> bytes:
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                         length=32,
                         salt=str1.encode('utf-8'),
                         iterations=100000,
                         backend=default_backend())
        passwd = str2 + ''.join(strs)
        key = urlsafe_b64encode(kdf.derive(passwd.encode('utf-8')))
        return key


class CipherInvalidToken(Exception):
    """
    Wrapper around actual implementation's decryption exceptions
    """
    pass
