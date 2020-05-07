#!/usr/bin/env python3
""""
 ****************************************************************************
 Filename:          decisiondb.py
 Description:       File for Repo Class for Decision Model.

 Creation Date:     21/04/2020
 Author:            Ajay Paratmandali

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

from eos.utils.data.access import Query
from eos.utils.data.access.filters import Compare
from eos.utils.data.db.db_provider import DataBaseProvider, GeneralConfig
from eos.utils.ha.dm.models.decisiondb import DecisionModel
from eos.utils.schema import database
from eos.utils.log import Log

class DecisionDB:
    """
    The class encapsulates decision management activities.
    This is intended to be used during decision management
    """

    def __init__(self) -> None:
        conf = GeneralConfig(database.DATABASE)
        self.storage = DataBaseProvider(conf)

    async def store_event(self, entity, entity_id, component, component_id,
                          alert_time, action):
        """
        Stores Data in Decision DB in Consul.
        :param entity: Entity Name :type: Str
        :param entity_id: Entity Id :type: Str
        :param component: Component Name :type: Str
        :param component_id: Component Id :type: Str
        :param alert_time: Alert Generated time :type: Str
        :param action: Action for the Component :type: Str
        :return:
        """
        # Generate Key
        decision_id = DecisionModel.create_decision_id(entity, entity_id,
                                                       component, component_id,
                                                       alert_time)
        Log.debug(f"Loading event for {decision_id} Action:- {action}")
        # Generate Decision DB Object.
        decision = DecisionModel.instantiate_decision(decision_id=decision_id,
                                                      action=action,
                                                      alert_time=alert_time)
        # Save Data.
        await self.storage(DecisionModel).store(decision)

    async def get_event(self, entity, entity_id, component, component_id,
                        alert_time):
        """
        Get a event with specific time.
        :param entity: Entity Name :type: Str
        :param entity_id: Entity Id :type: Str
        :param component: Component Name :type: Str
        :param component_id: Component Id :type: Str
        :param alert_time: Alert Generated time :type: Str
        :return: action For Respective Alert :type: Str
        """
        # Generate Key
        decision_id = DecisionModel.create_decision_id(entity, entity_id,
                                                       component, component_id,
                                                       alert_time)
        Log.debug(f"Fetch event for {decision_id}")
        # Create Query
        query = Query().filter_by(
            Compare(DecisionModel.decision_id, '=', decision_id))
        return await self.storage(DecisionModel).get(query)

    async def get_event_time(self, entity, entity_id, component, component_id,
                             **kwargs):
        """
        Fetch All Event with All Components Name.
        :param entity: Entity Name :type: Str
        :param entity_id: Entity Id :type: Str
        :param component: Component Name :type: Str
        :param component_id: Component Id :type: Str
        :return:
        """
        # Generate Key
        decision_id = DecisionModel.create_decision_id(entity, entity_id,
                                                       component, component_id)
        Log.debug(f"Fetch event time for {decision_id}")
        # Create Query
        query = Query().filter_by(
            Compare(DecisionModel.decision_id, 'like', decision_id))

        if kwargs.get("sort_by"):
            query.order_by(kwargs["sort_by"].field, kwargs['sort_by'].order)

        return await self.storage(DecisionModel).get(query)

    async def delete_event(self, entity, entity_id, component, component_id):
        """
        Delete all Component Related Events.
        :param entity: Entity Name :type: Str
        :param entity_id: Entity Id :type: Str
        :param component: Component Name :type: Str
        :param component_id: Component Id :type: Str
        :return:
        """
        # Generate Key
        decision_id = DecisionModel.create_decision_id(entity, entity_id,
                                                       component, component_id)
        Log.debug(f"Deleting event for {decision_id}")
        # Delete all the Decisions Related to The Event.
        await self.storage(DecisionModel).delete(
            Compare(DecisionModel.decision_id, 'like', decision_id))
