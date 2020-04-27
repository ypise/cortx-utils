#!/usr/bin/env python3
"""
 ****************************************************************************
 Filename:          provisioner.py
 Description:       This module will make use of provisioner configs to fetch
                    information related to the system.

 Creation Date:     04/25/2020
 Author:            Pawan Kumar Srivastava

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""
from eos.utils import const
try:
    from salt import client
except ModuleNotFoundError:
    client = None

"""
Provisioner class will contain methods to fetch configuration values from
valious provising configs like cluster.sls, sspl.sls etc.
"""
class Provisioner:
    @staticmethod
    def init():
        """
        Loading cluster.sls into memory.
        """
        Provisioner.cluster_config = dict()
        if client:
            Provisioner.cluster_config = client.Caller().function(const.PILLAR_GET\
                , const.CLUSTER)

    @staticmethod
    def get_data_nw_interface(node_id):
        """
        This method gets the data network interface
        """
        interface = []
        if Provisioner.cluster_config:
            interface = Provisioner.cluster_config.get(node_id).get\
                (const.NETWORK).get(const.DATA_NW).get(const.IFACE)
        return interface

    @staticmethod
    def get_mgmt_nw_interface(node_id):
        """
        This method gets the data network interface
        """
        interface = []
        if Provisioner.cluster_config:
            interface = Provisioner.cluster_config.get(node_id).get\
                (const.NETWORK).get(const.MGMT_NW).get(const.IFACE)
        return interface
