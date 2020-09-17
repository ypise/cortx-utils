#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          cron.py
 Description:       Contains the Class to Create Cron Jobs.

 Creation Date:     17/07/2020
 Author:            Prathamesh Rodi

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

import datetime
from crontab import CronTab
from eos.utils.log import Log


class CronJob:
    """
    Class to Schedule Cron Jobs
    """

    def __init__(self, user):
        try:
            self._cron = CronTab(user=user)
        except OSError as e:
            Log.error(f"Cron User Error : {e}")
            self._cron = None

    def create_run_time(self, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        """
        Create Running time for Cron Jobs
        :return: Extended time from Current Time.
        """
        return datetime.datetime.now() + datetime.timedelta(days, seconds, microseconds, milliseconds, minutes, hours,
                                                            weeks)

    def create_new_job(self, command, comment, schedule_time):
        """
        Creeate new Cron jobs
        :param command: Command to be Executed in Cron job.
        :param comment: Comment for Cron Job.
        :param schedule_time: time at which cron should be executed.
        :return:
        """
        if not self._cron:
            Log.error("Cron Job Object is not Instantiated")
            return
        Log.debug(f"Creating cron job for comment {comment}")
        _job = self._cron.new(command=command, comment=comment)
        _job.setall(schedule_time)
        self._cron.write()

    def remove_job(self, comment):
        """
        Remove Running/Scheduled Cron Jobs.
        :param comment: Comment for Cron Job. :type: String
        :return:
        """
        if not self._cron:
            Log.error("Cron Job Object is not Instantiated")
            return
        Log.debug(f"Removing cron job for comment {comment}")
        cron_jobs = self._cron.find_comment(comment)
        for each_job in cron_jobs:
            self._cron.remove(each_job)
            self._cron.write()
