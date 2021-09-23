from python_helper import log
from python_framework import Scheduler, SchedulerMethod, SchedulerType

from config import MessageConfig

@Scheduler()
class MessageScheduler :

    @SchedulerMethod(SchedulerType.INTERVAL, minutes=MessageConfig.SCHEDULE_CURRENT_SCANNING_MESSAGE_MINUTES_INTERVAL, instancesUpTo=1)
    def cleanCurrentScanningMessageDictionary(self) :
        self.service.message.cleanCurrentScanningMessageDictionary()
