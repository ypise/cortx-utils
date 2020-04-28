#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          test_decisiondb.py
 Description:       Test the Decision DB Methods.

 Creation Date:     18/04/2020
 Author:            Prathamesh Rodi


 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - : 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

import os
import asyncio
import unittest
from eos.utils.schema.payload import Json
from eos.utils.ha.dm.repository.decisiondb import DecisionDB
dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, 'test_schema', 'test_decisiondb_data.json')
TEST_DATA = Json(file_path).load()

class TestDecisionDB(unittest.TestCase):
    _dm = DecisionDB()
    _loop = asyncio.get_event_loop()

    def test_store_event(self):
        test_data = TEST_DATA.get("store_event", {})
        data = self._loop.run_until_complete(self._dm.store_event(
            **test_data.get('input')))
        self.assertEqual(data, test_data.get("output", ""))

    def test_get_event(self):
        test_data = TEST_DATA.get("get_event", {})
        data = self._loop.run_until_complete(
            self._dm.get_event(**test_data.get('input')))
        for actual, expected in zip(data, test_data.get("output")):
            self.assertDictEqual(actual.to_primitive(), expected)

    def test_get_event_time(self):
        test_data = TEST_DATA.get("get_event_time", {})
        data = self._loop.run_until_complete(self._dm.get_event_time(
            **test_data.get('input')))
        for actual, expected in zip(data, test_data.get("output")):
            print(actual.to_primitive(), expected)
            actual_value = actual.to_primitive()
            self.assertDictEqual(actual_value , expected)

    def test_delete_event(self):
        test_data = TEST_DATA.get("delete_event", {})
        data = self._loop.run_until_complete(self._dm.get_event_time(
            **test_data.get('input')))
        self.assertEqual(data, test_data.get("output"))

    def test_get_entity_health(self):
        test_data = TEST_DATA.get("delete_event", {})
        data = self._loop.run_until_complete(self._dm.get_event_time(
            **test_data.get('input')))
        for actual, expected in zip(data, test_data.get("output")):
            print(actual.to_primitive(), expected)
            actual_value = actual.to_primitive()
            self.assertDictEqual(actual_value , expected)

if __name__ == '__main__':
    unittest.main()
