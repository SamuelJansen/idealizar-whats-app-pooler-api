from python_helper import log
from python_framework import Scheduler, SchedulerMethod, SchedulerType

from config import WhatsAppWebConfig

@Scheduler()
class WhastAppWebScheduler :

    @SchedulerMethod(SchedulerType.INTERVAL, minutes=WhatsAppWebConfig.SCHEDULE_PING_MINUTES_INTERVAL, instancesUpTo=1)
    def pingBrowser(self) :
        self.service.whatsAppWeb.pingBrowser()
