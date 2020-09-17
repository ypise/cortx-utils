#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          node_status.py
 Description:       Model Class File for Maintainig Node Status

 Creation Date:     21/04/2020
 Author:            Prathamesh Rodi

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - : 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

from schematics.types import StringType, IntType
from eos.utils.ha.dm.models.base import HAModel

class NodeStatusModel(HAModel):
    _id = "node_id"

    node_id = StringType()
    io_failure_count = IntType()
    management_failure_count = IntType()

    @staticmethod
    def create_model_obj(node_id, **status_payload):
        """
        Create Model Object for Node Status Model
        :param node_id: Node Id :type: Str
        :param status_payload: Payload or remaining keys for Model :type: Dict
        :return: Model Object :type NodeStatusModel
        """
        node_status = NodeStatusModel()
        node_status.node_id = node_id
        node_status.io_failure_count = status_payload.get('io_failure_count', 0)
        node_status.management_failure_count = status_payload.get(
            'management_failure_count', 0)
        return node_status
