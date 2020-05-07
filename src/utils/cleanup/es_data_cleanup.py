#!/usr/bin/python3

"""
 ****************************************************************************
 Filename:          es_data_cleanup.py
 Description:       Remove old elasticsearch data from indexes helper script

 Creation Date:     03/03/2020
 Author:            Mazhar Inamdar

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

from datetime import datetime, timedelta
import requests
import io
import argparse
import traceback
import sys
import os
import pathlib
import json
from logging.handlers import SysLogHandler
import logging

class esCleanup(object):

    def __init__(self, service_name, path):
        self._path = path
        self.logger = self.get_logger(service_name, path)

    def remove_old_data_from_indexes(self, days, host, indexes, field):
        self.logger.debug(f'Will keep data from indexes for [{days}] days')
        date_N_days_ago = datetime.now() - timedelta(days=days)
        date_dago = str(datetime.strftime(date_N_days_ago, '%Y.%m.%d'))
        self.logger.debug(f'Will remove all data from indexes earlier than [{date_dago}]')
        headers = {'Content-type': 'application/json'}
        d = {  "query": {  "range" : {
               f"{field}": {
                 "lt" :  f"now-{days}d"
            }
        } } }
        for index in indexes:
            try:
                response = requests.post(f'http://{host}/{index}/_delete_by_query', 
                                                              data = json.dumps(d), headers = headers) 
            except Exception as e:
                self.logger.error(f'ERROR: cannot delete data for {index}', traceback.format_exc())
            if response.status_code == 200:
                res = json.loads(response.text)
                self.logger.info(f'deleted {res.get("total",0)} old record from {index} resp: {response.text}')
        return

    def get_logger(self, filename, path):
        """ check/create directory for common logs"""
        try:
            if not os.path.exists(path): os.makedirs(path)
        except OSError as err:
            if err.errno != errno.EEXIST: raise
        # added hardcoded logger "util_log" to avoid duplicate log
        # in csm_cleanup.log
        logger = logging.getLogger("util_log")
        logger.setLevel(logging.INFO)
        format = '%(name)s %(levelname)s %(message)s'
        formatter = logging.Formatter(format)
        fh = logging.FileHandler(os.path.join(path, f"{filename}.log"))
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    # Remove selected index from es db
    def remove_by_index(self, host, index):
        response = requests.delete(f'http://{host}/{index}')
        if response.status_code == 200:
            self.logger.debug(f'index {index} removed successfully')
        else:
            self.logger.error(f'error removing index {index} :{response.status_code}')
        return response.status_code

