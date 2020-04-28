#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          database.py
 Description:      Database Config File for Py-utils Library.

 Creation Date:     17/4/2020
 Author:            Prathamesh Rodi

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - : 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

DATABASE = {
    "databases": {
        "consul_db": {
            "import_path": "ConsulDB",
            "config": {
                "host": "localhost",
                "port": 8500,
                "login": "",
                "password": ""
            }
        }
    },
    "models": [
        {
            "import_path": "eos.utils.ha.dm.models.decisiondb.DecisionModel",
            "database": "consul_db",
            "config": {
                "consul_db": {
                    "collection": "HA"
                }
            }
        }

    ]
}
