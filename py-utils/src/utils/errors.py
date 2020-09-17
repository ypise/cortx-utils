"""
 ****************************************************************************
 Filename:          errors.py
 _description:      Errors for various CLI related scenarios.

 Creation Date:     31/05/2018
 Author:            Malhar Vora
                    Ujjwal Lanjewar

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

import inspect

OPERATION_SUCESSFUL = 0x0000
INTERNAL_ERROR = 0x1005


class BaseError(Exception):
    """ Parent class for the cli error classes """

    _rc = OPERATION_SUCESSFUL
    _desc = 'Operation Successful'
    _caller = ''

    def __init__(self, rc=0, desc=None, message_id=None, message_args=None):
        super(BaseError, self).__init__()
        self._caller = inspect.stack()[1][3]
        if rc is not None:
            self._rc = str(rc)
        self._desc = desc or self._desc
        self._message_id = message_id
        self._message_args = message_args

    def message_id(self):
        return self._message_id

    def message_args(self):
        return self._message_args

    def rc(self):
        return self._rc

    def error(self):
        return self._desc

    def caller(self):
        return self._caller

    def __str__(self):
        return "error(%s): %s" % (self._rc, self._desc)


class InternalError(BaseError):
    """
    This error is raised by CLI for all unknown internal errors
    """

    def __init__(self, desc=None, message_id=None, message_args=None):
        super(InternalError, self).__init__(
              INTERNAL_ERROR, 'Internal error: %s' % desc,
              message_id, message_args)


class DataAccessError(InternalError):

    """Base Data Access Error"""


class DataAccessExternalError(DataAccessError):

    """Internal DB errors which happen outside of db framework"""


class DataAccessInternalError(DataAccessError):

    """Errors regarding db framework part of Data Access implementation"""


class MalformedQueryError(DataAccessError):

    """Malformed Query or Filter error"""


class MalformedConfigurationError(DataAccessError):

    """Error in configuration of data bases or storages or db drivers"""


class StorageNotFoundError(DataAccessError):

    """Model object is not associated with any storage"""

class AmqpConnectionError(Exception):

    """Amqp connection problems"""
