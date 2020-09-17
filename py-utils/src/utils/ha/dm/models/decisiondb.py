#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          decisiondb.py
 Description:       decisionDB Model File

 Creation Date:     15/4/2020
 Author:            Ajay Paratmandali
                    Prathamesh Rodi

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - : 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

from schematics.types import StringType, DateTimeType

from eos.utils.ha.dm.models.base import HAModel

class DecisionModel(HAModel):
    _id = "decision_id"

    decision_id = StringType()
    action = StringType()
    alert_time = DateTimeType()

    @staticmethod
    def create_decision_id(*decision_payload):
        """
        This method creates the key for Decision DB.
        :param decision_payload: Parameters for Decision Payload. :type: Tuple
        :return:
        """
        return "/".join(decision_payload)

    @staticmethod
    def instantiate_decision(**decision_payload):
        """
        Generate the Decision DB model object.
        :param decision_payload: Data For Decision DB.
        :return:
        """
        decision = DecisionModel()
        decision.decision_id = decision_payload.get("decision_id", "")
        decision.action = decision_payload.get("action", "")
        decision.alert_time = decision_payload.get("alert_time", "")
        return decision
