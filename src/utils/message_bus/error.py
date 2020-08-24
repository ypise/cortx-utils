#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          error.py
 Description:       Error handling class for Messagebus module.
 Creation Date:     10/08/2020
 Author:            Pawan Kumar Srivastava
 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

from eos.utils.errors import BaseError
from eos.utils.log import Log

OPERATION_SUCCESSFUL    = 0x0000
CONNECTION_ERROR        = 0x1001
INTERNAL_ERROR          = 0x1002
INVALID_CONFIG          = 0x1003
SEND_ERROR              = 0x1004
MSG_FETCH_ERROR         = 0x1005
NO_MSG_ERROR            = 0x1006

class MessagebusError(BaseError):
    """
    Parent class for the Messagebus error classes
    """

    def __init__(self, rc=0, desc=None, message_id=None, message_args=None):
        super(MessagebusError, self).__init__(rc=rc, desc=desc, message_id=message_id,
                                       message_args=message_args)
        Log.error(f"{self._rc}:{self._desc}:{self._message_id}:{self._message_args}")

class InvalidConfigError(MessagebusError):
    """
    This error will be raised when an invalid config is recevied.
    """

    _err = INVALID_CONFIG
    _desc = "MessagebusError: Invalid config received."

    def __init__(self, _desc=None, message_id=None, message_args=None):
        super(InvalidConfigError, self).__init__(
            INVALID_CONFIG, _desc, message_id, message_args)

class OperationSuccessful:
    """
    This will be raised when an operation is successfull.
    """
    def __init__(self, desc):
        self._rc = OPERATION_SUCCESSFUL
        self._desc = desc

    def msg(self):
        return f"MessagebusSuccess({self._rc}) : {self._desc}"

class ConnectionEstError(MessagebusError):
    """
    This error will be raised when connection could not be established.
    """

    _err = CONNECTION_ERROR
    _desc = "MessagebusError: Connection establishment failed."

    def __init__(self, _desc=None, message_id=None, message_args=None):
        super(ConnectionEstError, self).__init__(
            CONNECTION_ERROR, _desc, message_id, message_args)

class SendError(MessagebusError):
    """
    This error will be raised when message sending is failed.
    """

    _err = SEND_ERROR
    _desc = "MessagebusError: Message sending failed."

    def __init__(self, _desc=None, message_id=None, message_args=None):
        super(SendError, self).__init__(
            SEND_ERROR, _desc, message_id, message_args)

class NoMsgError(MessagebusError):
    """
    This error will be raised when no message is fetch.
    """

    _err = NO_MSG_ERROR
    _desc = "MessagebusError: No Message to deliver."

    def __init__(self, _desc=None, message_id=None, message_args=None):
        super(NoMsgError, self).__init__(
            NO_MSG_ERROR, _desc, message_id, message_args)

class MsgFetchError(MessagebusError):
    """
    This error will be raised when no message is fetch.
    """

    _err = MSG_FETCH_ERROR
    _desc = "MessagebusError: Error occured in fetching message."

    def __init__(self, _desc=None, message_id=None, message_args=None):
        super(MsgFetchError, self).__init__(
            MSG_FETCH_ERROR, _desc, message_id, message_args)
