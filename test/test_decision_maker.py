#!/usr/bin/env python3

import os
import unittest
from unittest.mock import MagicMock
import asyncio

from eos.utils.ha.dm.decision_maker import DecisionMaker
from eos.utils.schema.payload import Json, JsonMessage
from eos.utils.ha.dm.repository.decisiondb import DecisionDB

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, 'test_alert.json')
rules_schema_path = os.path.join(dir_path, 'rules_engine_schema.json')

class TestDecisionMaker(unittest.TestCase):
    """Module to test DecisionMaker class"""

    res_to_entity_mapping = {
        "enclosure": ("enclosure", "connectivity"),
        "enclosure:fru:controller": ("enclosure", "controller")
        }

    mock_decisiondb = DecisionDB()
    _dec_maker = DecisionMaker(decisiondb=mock_decisiondb)
    json_alert_data = Json(file_path).load()
    rules_data = Json(rules_schema_path).load()
    _loop = asyncio.get_event_loop()

    def test_handle_alert(self):
        """tests handle_alert functio of DecisionMaker class"""

        assert self.json_alert_data is not None
        self.assertTrue(isinstance(self.json_alert_data, dict))
        self._loop.run_until_complete(self._dec_maker.handle_alert(self.json_alert_data))
        res_type = self.json_alert_data["message"]["sensor_response_type"]["info"]["resource_type"]
        res_id = self.json_alert_data["message"]["sensor_response_type"]["info"]["resource_id"]
        node_id = self.json_alert_data["message"]["sensor_response_type"]["info"]["node_id"]
        host_id = self.json_alert_data["message"]["sensor_response_type"]["host_id"]
        event_time = self.json_alert_data["message"]["sensor_response_type"]["info"]["event_time"]
        alert_type = self.json_alert_data["message"]["sensor_response_type"]["alert_type"]
        severity = self.json_alert_data["message"]["sensor_response_type"]["severity"]
        tuple_val = self.res_to_entity_mapping[res_type]
        entity, component = tuple_val[0], tuple_val[1]
        if entity == "enclosure":
            entity_id = '0'
        else:
            entity_id = host_id
        if res_type == "enclosure":
            component_id = host_id
        else:
            component_id = res_id

        action = ''
        res_type_data = self.rules_data[res_type]
        if res_type_data is not None:
            for item in res_type_data:
                if alert_type == item["alert_type"] and \
                    severity == item["severity"]:
                    action = item["action"]

        self.mock_decisiondb.store_event.assert_called_with(entity, entity_id, \
            component, component_id, event_time, action)

if __name__ == '__main__':
    unittest.main()
