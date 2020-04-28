#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          node_status.py
 Description:       Repository Class File for Node_status Model

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

from eos.utils.data.access import Query
from eos.utils.data.access.filters import Compare
from eos.utils.data.db.db_provider import DataBaseProvider, GeneralConfig
from eos.utils.ha.dm.models.node_status import NodeStatusModel
from eos.utils.schema import database
from eos.utils.ha.dm.actions import Action

class NodeStatusDB:
    def __init__(self) -> None:
        conf = GeneralConfig(database.DATABASE)
        self.storage = DataBaseProvider(conf)

    async def get(self, node_id):
        """
        Get Individual Node Status for Provided Node Id.
        :param node_id: Node_id :type str
        :return: List[NodeStatusModel]
        """
        query = Query().filter_by(
            Compare(NodeStatusModel.node_id, '=', node_id)
        )

        return await self.storage(NodeStatusModel).get(query)

    async def update(self, node_id, **kwargs):
        """
        Update Provided Data for given Node Id.
        :param node_id: Node_id :type str
        :param kwargs: Keys to be Updated :type:Dict
        :return: True/False for Updated/Not-Updated
        """
        query = Query().filter_by(
            Compare(NodeStatusModel.node_id, '=', node_id)
        )
        return await self.storage(NodeStatusModel).update(query, kwargs)

    async def create(self, node_id, **kwargs):
        """
        Create a Node_Status Object in Consul for Given Node ID
        :param node_id: Node_id :type str
        :param kwargs: Keys to be Updated :type:Dict
        :return: True/False for Created/Not-Created
        """
        model_obj = NodeStatusModel.create_model_obj(node_id, **kwargs)
        return await self.storage(NodeStatusModel).store(model_obj)

    async def update_io_count(self, node_id, action):
        """
        Updates IO Failure Count for Provided Node_ID
        :param node_id: Node_id :type str
        :param action: 'Failed/Resolved' For IO Path.
        :return:
        """
        node_status = await self.get(node_id)
        io_count = 0
        # If Node Status is Not Present Create it.
        if not node_status:
            if action == Action.FAILED:
                io_count = 1
            return await self.create(node_id, io_failure_count=io_count)
        else:
            if action == Action.FAILED:
                io_count = node_status[0].io_failure_count + 1
            if action ==  Action.RESOLVED and node_status[0].io_failure_count != 0:
                io_count = node_status[0].io_failure_count - 1
            return await self.update(node_id, io_failure_count=io_count)

    async def update_mgmt_count(self, node_id, action):
        """
        Updates Management Failure Count for Provided Node_ID
        :param node_id: Node_id :type str
        :param action: 'Failed/Resolved' For Management Path.
        :return:
        """
        node_status = await self.get(node_id)
        io_count = 0
        if not node_status:
            if action == Action.FAILED:
                io_count = 1
            return await self.create(node_id, management_failure_count=io_count)
        else:
            if action == Action.FAILED :
                io_count = node_status[0].io_failure_count + 1
            if action == Action.RESOLVED and node_status[
                0].management_failure_count != 0:
                io_count = node_status[0].management_failure_count - 1
            await self.update(node_id, management_failure_count=io_count)
