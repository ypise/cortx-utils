"""
 ****************************************************************************
 Filename:          secure_storage.py
 Description:       Storage of explicitly AES encrypted objects upon Consul KVS

 Creation Date:     02/03/2019
 Author:            Alexander Voronov

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""


from schematics.types import StringType

from eos.utils.security.cipher import Cipher
from eos.utils.db.base_model import BaseModel
from eos.utils.db.filters import Compare
from eos.utils.db.queries import Query
from eos.utils.db.storage import AbstractDataBaseProvider


class NamedEncryptedBytes(BaseModel):
    """
    Encrypted bytes model
    """

    _id = "name"

    name = StringType()
    data = StringType()

    @staticmethod
    def instantiate(name: str, data: str):
        """
        Creates an NamedEncryptedBytes instance
        """

        neb = NamedEncryptedBytes()
        neb.name = name
        neb.data = data
        return neb


class SecureStorage:
    """
    Storage of explicitly EOS cipher encrypted objects upon Consul KVS
    """

    def __init__(self, storage: AbstractDataBaseProvider, key: bytes) -> None:
        self._storage = storage
        self._key = key

    async def _get_item(self, name: str) -> NamedEncryptedBytes:
        """
        Gets NamedEncryptedBytes object with encrypted payload from the storage

        Returns NamedEncryptedBytes object if the item with provided name exists or None
        """

        query = Query().filter_by(Compare(NamedEncryptedBytes.name, '=', name))
        neb = next(iter(await self._storage(NamedEncryptedBytes).get(query)), None)
        return neb

    async def store(self, name: str, data: bytes, force=False) -> None:
        """
        Saves the data to the encrypted storage

        Data is AES encrypted with the default EOS cipher and stored
        as Base64 encoded string with the provided name.
        Raises KeyError if an item with the provided name exists and "force" flag
        is not set.
        """

        if not force:
            neb = await self._get_item(name)
            if neb is not None:
                raise KeyError(f'{name} already exists in the secure storage')

        encrypted_bytes = Cipher.encrypt(self._key, data)
        # Encrypted token is base64 encoded, thus there won't be a problem with storing it in String
        neb = NamedEncryptedBytes.instantiate(name, encrypted_bytes.decode('ascii'))
        await self._storage(NamedEncryptedBytes).store(neb)

    async def get(self, name: str) -> bytes:
        """
        Gets bytes from the encrypted storage

        Acquires the data from the storage and decrypts it with the default EOS cipher
        Raises EosCipherInvalidToken if decryption fails.
        """

        neb = await self._get_item(name)
        if neb is None:
            return None

        decrypted_bytes = Cipher.decrypt(self._key, neb.data.encode('ascii'))
        return decrypted_bytes

    async def delete(self, name: str) -> None:
        """
        Removes the data from the encrypted storage
        """

        neb = await self._get_item(name)
        if neb is None:
            raise KeyError(f'Item "{name}" was not found in secure storage')
        await self._storage(NamedEncryptedBytes).delete(Compare(NamedEncryptedBytes.name, '=', name))
