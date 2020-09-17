#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          comm.py
 Description:       Contains interfaces for communication and channel classes
 Creation Date:     05/08/2020
 Author:            Sandeep Anjara
 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

from abc import ABCMeta, abstractmethod

class Channel(metaclass=ABCMeta):

    """Abstract class to represent a comm channel to a node"""

    @abstractmethod
    def init(self):
        raise Exception('init not implemented in Channel class')

    @abstractmethod
    def connect(self):
        raise Exception('connect not implemented in Channel class')

    @abstractmethod
    def disconnect(self):
        raise Exception('disconnect not implemented in Channel class')

    @abstractmethod
    def send(self, message):
        raise Exception('send not implemented in Channel class')

    @abstractmethod
    def send_file(self, local_file, remote_file):
        raise Exception('send_file not implemented in Channel class')

    @abstractmethod
    def recv(self, message=None):
        raise Exception('recv not implemented in Channel class')

    @abstractmethod
    def recv_file(self, remote_file, local_file):
        raise Exception('recv_file not implemented in Channel class')

    @abstractmethod
    def acknowledge(self, delivery_tag=None):
        raise Exception('acknowledge not implemented for Channel class')


class Comm(metaclass=ABCMeta):

    """Abstract class to represent a comm channel"""

    @abstractmethod
    def init(self):
        raise Exception('init not implemented in Comm class')

    @abstractmethod
    def connect(self):
        raise Exception('connect not implemented in Comm class')

    @abstractmethod
    def disconnect(self):
        raise Exception('disconnect not implemented in Comm class')

    @abstractmethod
    def send(self, message, **kwargs):
        raise Exception('send not implemented in Comm class')

    @abstractmethod
    def send_message_list(self, message: list, **kwargs):
        raise Exception('send_message_list not implemented in Comm class')

    @abstractmethod
    def recv(self, callback_fn=None, message=None, **kwargs):
        raise Exception('recv not implemented in Comm class')

    @abstractmethod
    def acknowledge(self):
        raise Exception('acknowledge not implemented in Comm class')
