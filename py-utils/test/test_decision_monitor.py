#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          test_decision_monitor.py
 Description:       Test Cases for Decision Monitor

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
import datetime
import os
import unittest

from eos.utils.ha.dm.decision_monitor import DecisionMonitor
from eos.utils.ha.dm.repository.decisiondb import DecisionDB
from eos.utils.schema.payload import Json

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, 'test_schema', 'test_decision_monitor_data.json')
TEST_DATA = Json(file_path).load()

def _generate_data():
    d = DecisionDB()
    for index, each_input in enumerate(TEST_DATA.get("input", [])):
        each_input["alert_time"] = str(
            datetime.datetime.now() + datetime.timedelta(hours=index))
        d.store_event(**each_input)

class TestDecisionMonitor(unittest.TestCase):
    _dm = DecisionMonitor()
    _dm._resource_file = TEST_DATA.get("test_file")
    _loop = asyncio.get_event_loop()
    _generate_data()

    def test_resource_group(self):
        data = self._loop.run_until_complete(
            self._dm.get_resource_group_status("io_c1"))
        self.assertEqual("resolved", data)

    def test_acknowledge_resource_group(self):
        data = self._loop.run_until_complete(
            self._dm.acknowledge_resource_group("io_c1"))
        self.assertIsNone(data)

if __name__ == '__main__':
    unittest.main()
