#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          decision_monitor.py
 Description:       Decision Monitor Class File.

 Creation Date:     23/04/2020
 Author:            Prathamesh Rodi

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - : 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

import asyncio
import os
from typing import AnyStr

from eos.utils.ha.dm.repository.decisiondb import DecisionDB
from eos.utils.ha.dm.models.decisiondb import DecisionModel
from eos.utils.ha.dm.actions import Action
from eos.utils.ha.hac import const
from eos.utils.schema.payload import Json
from eos.utils.errors import DataAccessInternalError
from eos.utils.log import Log
from eos.utils.data.access import SortBy, SortOrder

class DecisionMonitor:
    """
    Fetch Resource Decisions from Decision DB.
    """

    def __init__(self):
        self._decisiondb = DecisionDB()
        self._resource_file = Json(
            os.path.join(const.CONF_PATH, const.DECISION_MAPPING_FILE)).load()
        self._loop = asyncio.get_event_loop()

    def get_resource_status(self, resource: AnyStr):
        """
        Get the Status for Resource
        :param resource: Name of Resource :type: str
        :return:
        """
        resource_key = self._resource_file.get("resources", {}).get(resource, {})
        try:
            resource_data = self._loop.run_until_complete(
                self._decisiondb.get_event_time(**resource_key,
                    sort_by=SortBy(DecisionModel.alert_time, SortOrder.DESC)))
        except Exception as e:
            # Return OK if Failed to Fetch Resource Status.
            Log.error(f"{e}")
            return Action.OK
        if resource_data:
            return resource_data[0].action
        return Action.OK

    def get_resource_group_status(self, resource_group):
        """
        Fetch Resource Group Status.
        :param resource_group: Name of Resource Group.
        :return:
        """
        group_status = []
        # Fetch List of Resources in group
        resources = self._resource_file.get("resource_groups", {}).get(
            resource_group, [])
        for resource in resources:
            # Check's the status for each resource.
            status = self.get_resource_status(resource)
            if status in [Action.FAILED]:
                # Return Failed if any one is Failed Status in RG.
                return status
            group_status.append(status)
        if Action.RESOLVED in group_status:
            #  Return Resolved if none is Failed and any one is resolved Status in RG.
            return Action.RESOLVED
        return Action.OK

    def acknowledge_resource(self, resource):
        """
        Acknowledge a Single Resource Group.
        :param resource:
        :return:
        """
        resource_key = self._resource_file.get("resources", {}).get(resource, {})
        try:
            if not self.get_resource_status(resource) == Action.FAILED:
                self._loop.run_until_complete(
                    self._decisiondb.delete_event(**resource_key))
        except Exception as e:
            Log.error(f"{e}")

    def acknowledge_resource_group(self, resource_group):
        """
        Acknowledge a Single Resource Group.
        :param resource_group:
        :return:
        """
        resources = self._resource_file.get("resource_groups", {}).get(
            resource_group, [])
        for resource in resources:
            self.acknowledge_resource(resource)
