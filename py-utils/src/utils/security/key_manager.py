"""
 ****************************************************************************
 Filename:          key_manager.py
 Description:       Manager for security material.

 Creation Date:     12/20/2019
 Author:            Alexander Voronov

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

from os import stat, umask
from pathlib import Path, PosixPath
from types import TracebackType
from typing import Optional, Type


class KeyMaterialStore:
    """
    Context manager for safe access to key material store.
    """
    _old_umask: int
    _store_path: Path

    def __init__(self, store_path: str) -> None:
        self._store_path = PosixPath(store_path)

    def __enter__(self) -> 'KeyMaterialStore':
        self._old_umask = umask(0o077)
        self._store_path.mkdir(parents=True, exist_ok=True)
        if stat(self._store_path).st_mode & 0o077:
            umask(self._old_umask)
            raise Exception(f'Key store "{self._store_path}" has lax permissions')
        umask(0o177)
        return self

    def __exit__(
        self,
        exception_type: Optional[Type[BaseException]],
        exception_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        umask(self._old_umask)

    def path(self) -> Path:
        """
        Returns the path to the key material store.

        :return: Path to the key material store
        """
        return self._store_path

    def resolve_path(self, relative_path: str, lax: bool = False) -> Path:
        """
        Resolves paths in the key material store, checking for lax permissions.

        :param relative_path: Relative path inside the key material store
        :param lax: Check for lax permissions if `False`
        :return: Resolved path
        """
        path = PosixPath(self._store_path) / relative_path
        path.resolve(strict=True)
        if not lax and stat(path).st_mode & 0o177:
            raise Exception(f'Key material "{relative_path}" has lax permissions.')
        return path
