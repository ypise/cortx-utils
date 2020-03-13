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

# Script will delete old data from indexes in elasticsearch
#
# days parameter - how many days before current date will be listed for deletion
#                  0 - means delete all even today's data
# host parameter - address and port of elasticsearch server
#
# config - change default parameters in __main__
#
# Use -h option to show help

from datetime import datetime, timedelta
import requests
import io
import argparse
import traceback
import sys
import os
import pathlib
import json

def remove_old_data_from_indexes(arg_d, arg_n, arg_i, arg_f):
    host = arg_n
    days = arg_d
    logger.debug(f'Will keep data from indexes for [{days}] days')
    date_N_days_ago = datetime.now() - timedelta(days=days)
    date_dago = str(datetime.strftime(date_N_days_ago, '%Y.%m.%d'))
    logger.debug(f'Will remove all data from indexes earlier than [{date_dago}]')
    headers = {'Content-type': 'application/json'}
    d = {  "query": {  "range" : {
               f"{arg_f}": {
                 "lt" :  f"now-{days}d"
            }
         } } }
    for index in arg_i:
        try:
            response = requests.post(f'http://{host}/{index}/_delete_by_query', 
                                                              data = json.dumps(d), headers = headers) 
        except Exception as e:
            logger.error(f'ERROR: cannot delete data for {index}', traceback.format_exc())
        if response.status_code == 200:
            res = json.loads(response.text)
            logger.info(f'deleted {res.get("total",0)} old record from {index} resp: {response.text}')
        return

if __name__ == '__main__':
    ES_CLEANUP_LOG = "/var/log/seagate/common/"    
    from logging.handlers import SysLogHandler
    import logging
    """ check/create directory for common logs""" 
    try:
        if not os.path.exists(ES_CLEANUP_LOG): os.makedirs(ES_CLEANUP_LOG)
    except OSError as err:
        if err.errno != errno.EEXIST: raise
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    format = '%(name)s %(levelname)s %(message)s'
    formatter = logging.Formatter(format)
    fh = logging.FileHandler(os.path.join(ES_CLEANUP_LOG, "es_data_cleanup.log"))
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    try:
        argParser = argparse.ArgumentParser(
            usage = "%(prog)s [-h] [-d] [-n] [-i] [-f]",
            formatter_class = argparse.RawDescriptionHelpFormatter)
        argParser.add_argument("-d", type=int, default=90,
                help="days to keep data")
        argParser.add_argument("-n", type=str, default="localhost:9200",
                help="address:port of elasticsearch service")
        argParser.add_argument("-f", type=str, default="timestamp",
                help="field of index of elasticsearch service")
        argParser.add_argument("-i", nargs='+', default=[],
                help="index of elasticsearch")
        args = argParser.parse_args()
        # Pass arguments to worker function
        # remove data older than given number of days
        remove_old_data_from_indexes(args.d, args.n, args.i, args.f)
    except Exception as e:
        logger.error(e, traceback.format_exc())
