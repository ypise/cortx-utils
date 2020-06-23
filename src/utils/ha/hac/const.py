#!/usr/bin/env python3

BUILD_PATH = "/tmp"
BASE_PATH = '/opt/seagate/cortx/ha/'
CONF_PATH = '/etc/cortx/ha/'
PROV_CONF_INDEX = "PROV_CONF_INDEX"
HAC_LOG = "/tmp/hac.log"
HA_MODES = ["active_passive", "active_active", "master_slave"]
HA_GROUP = ["common", "management", "io"]
IO_PATH = 'io'
MGMT_PATH = 'mgmt'
FAILED_STATUSES = ['failed']
DECISION_MAPPING_FILE = 'decision_monitor_conf.json'
HA_DATABADE_SCHEMA='database.json'