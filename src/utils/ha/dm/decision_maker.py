#!/usr/bin/env python3
"""
 ****************************************************************************
 Filename:          decision_maker.py
 Description:       HA Decision Maker module which takes decision based on
                    alert received from CSM. It stores the decision taken into
                    DecisionDB.

 Creation Date:     04/22/2020
 Author:            Madhura Mande
                    Pawan Kumar Srivastava

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

import errno
import json
import os
import asyncio

from eos.utils.log import Log
from eos.utils.schema.payload import JsonMessage, Json
from eos.utils import const
from eos.utils.ha.dm.repository.decisiondb import DecisionDB

class RuleEngine(object):
    """
    Module responsible for validating the alert against set of rules.
    """

    def __init__(self, rule_file=None):
        self._rule_file = rule_file
        self._rules_schema = None
        self._load_rules()

    def _load_rules(self):
        """
        Reads the json structured rule data from the file, and returns it
        in dict format.
        """
        rules_data = None
        try:
            if self._rule_file is None:
                return None
            Log.debug(f"Loading rules json into memory. File: {self._rule_file}")
            with open(self._rule_file, 'r') as fp:
                rules_data = fp.read()
            if rules_data:
                rules_json = JsonMessage(rules_data)
                self._rules_schema = rules_json.load()
        except OSError as os_error:
            if os_error.errno == errno.ENOENT:
                Log.error(f'File {self._rule_file} does not exist')
            elif os_error.errno == errno.EACCES:
                Log.error(f'Not enough permission to read {self._rule_file} file')
            else:
                Log.error(f'Error while reading from file {self._rule_file}')

    def evaluate_alert(self, alert):
        """
        Compares the alert with the predefined json structure and returns
        action such as fail-over, fail-back etc.
        """
        Log.debug(f"Evaluating alert: {alert}")
        action = None
        if not self._rules_schema:
            return action
        sensor_response = alert.get(const.MESSAGE).get(const.SENSOR_RES_TYPE)
        res_type = sensor_response.get(const.INFO).get(const.RESOURCE_TYPE)
        alert_type = sensor_response.get(const.ALERT_TYPE)
        severity = sensor_response.get(const.SEVERITY)
        if res_type is None:
            return action
        res_type_data = self._rules_schema[res_type]
        if res_type_data is not None:
            for item in res_type_data:
                if alert_type == item[const.ALERT_TYPE] and \
                    severity == item[const.SEVERITY]:
                    action = item[const.ACTION]
        Log.debug(f"Found {action} action for resource: {res_type} with alert type:\
            {alert_type} and severity: {severity}.")
        return action


class DecisionMaker(object):
    """
    This class is responsible for taking the HA decisions
    such as failover/failback with the help of RuleEngine
    """

    def __init__(self, decisiondb=DecisionDB()):
        self._rule_engine = RuleEngine(os.path.join(\
            const.CORTX_HA_INSTALL_PATH, const.RULES_FILE_PATH))
        self._decision_db = decisiondb
        self._conf = Json(os.path.join(\
            const.CORTX_HA_INSTALL_PATH, const.CONF_FILE_PATH)).load()

    async def _get_data_nw_interface(self, host_id):
        interface = []
        if self._conf:
            interface = self._conf.get(const.NETWORK).get(host_id).get\
                (const.DATA_IFACE)
        return interface

    async def _get_mgmt_nw_interface(self, host_id):
        interface = []
        if self._conf:
            interface = self._conf.get(const.NETWORK).get(host_id).get\
                (const.MGMT_IFACE)
        return interface

    async def _get_host_id(self, node_id):
        host_id = ""
        if self._conf:
            host_id = self._conf.get(const.NODES).get(node_id)
        return host_id

    async def handle_alert(self, alert):
        """
        Accepts alert in the dict format and validates the same
        alert against set of rules with the help of RuleEngine.
        """
        if alert is not None:
            action = self._rule_engine.evaluate_alert(alert)
            if action is not None:
                await self._store_action(alert, action)

    async def _store_action(self, alert, action):
        """
        Further parses the alert to store information such as:
        component: Actual Hw component which has been affected
        component_id: FRU_ID
        entity: enclosure/node
        entity_id: resource id
        """
        sensor_response = alert.get(const.MESSAGE).get(const.SENSOR_RES_TYPE)
        info_dict = await self._set_db_key_info(sensor_response)
        await self._decision_db.store_event(info_dict[const.ENTITY], \
            info_dict[const.ENTITY_ID], info_dict[const.COMPONENT], \
            info_dict[const.COMPONENT_ID], info_dict[const.EVENT_TIME], action)

    async def _set_db_key_info(self, sensor_response):
        """
        This function derives entity, entity_id, component, component_id,
        event_time from the incoming alert.
        These fields are required to create key for storing the decision in db.
        Key format -
        HA/entity/entity_id/component/component_Id/timestamp
        Examples -
        1. HA/Enclosure/0/controller/1/timestamp
        2. HA/Enclosure/0/controller/2/timestamp
        3. HA/Enclosure/0/fan/0/timestamp
        4. HA/Node/1/raid/0/timestamp
        5. HA/Node/0/IEM/mero/timestamp
        6. HA/Node/1/IEM/s3/timestamp
        """
        info_dict = dict()
        info = sensor_response.get(const.INFO)
        resource_type = info.get(const.RESOURCE_TYPE)
        resource_id = info.get(const.RESOURCE_ID)
        node_id = info.get(const.NODE_ID)
        host_id = await self._get_host_id(node_id)
        """
        1. Setting event time.
        """
        info_dict[const.EVENT_TIME] = info.get(const.EVENT_TIME)
        """
        Here resource type can be in 2 forms -
        1. enclosure:fru:disk, node:os:disk_space etc
        2. enclosure, iem
        Spliting the resource type will give us the entity and component fields.
        """
        res_list = resource_type.split(':')

        """
        2. Setting entity.
        For IEM alerts we do not get Node/Enclosure in resource type, so we
        have to hardcode it to node.
        """
        if resource_type == const.IEM:
            component_id = sensor_response.get(const.SPECIFIC_INFO).get\
                (const.COMPONENT_ID)
            info_dict[const.ENTITY] = const.NODE
            info_dict[const.COMPONENT] = resource_type
            info_dict[const.COMPONENT_ID] = component_id
        else:
            info_dict[const.ENTITY] = res_list[0]

        """
        3. Setting entity_id
        """
        if info_dict[const.ENTITY] == const.NODE:
            info_dict[const.ENTITY_ID] = host_id
        else:
            info_dict[const.ENTITY_ID] = "0"

        """
        4. Setting Component.
        We will check if we have got the component value in resource type.
        """
        if len(res_list) > 1:
            info_dict[const.COMPONENT] = res_list[2]
        else:
            """
            We have to perform some checks if component is not present in
            reource_type field.
            1. For storage connectivity we have component = connectivity
            2. For storage connectivity we have component_id = node/host id
            """
            if info_dict[const.ENTITY] == const.ENCLOSURE:
                info_dict[const.COMPONENT] = const.CONNECTIVITY
                info_dict[const.COMPONENT_ID] = host_id

        """
        5. Setting component id
        """
        if info_dict[const.COMPONENT] == const.CONTROLLER:
            info_dict[const.COMPONENT_ID] = host_id
        elif resource_type == const.NIC:
            """
            If resource_type is node:interface:nw, then we will read the values
            from config to know whether if is data or management interface.
            """
            info_dict[const.COMPONENT_ID] = await self._get_component_id_for_nic(\
                host_id, resource_id)
        elif resource_type not in (const.IEM, const.ENCLOSURE):
            """
            For IEM the component id is fetched from specific info's component
            id field
            """
            info_dict[const.COMPONENT_ID] = resource_id

        return info_dict

    async def _get_component_id_for_nic(self, host_id, resource_id):
        component_id = ""
        """
        First checking if resource is found in data_nw.
        """
        nw_interface = await self._get_data_nw_interface(host_id)
        if resource_id in nw_interface:
            component_id = const.DATA
        else:
            """
            Since resource not found in data_nw lets serach is mgmt_nw.
            """
            nw_interface = await self._get_mgmt_nw_interface(host_id)
            if resource_id in nw_interface:
                component_id = const.MGMT
        return component_id
