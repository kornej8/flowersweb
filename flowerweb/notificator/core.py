import os
import sys
sys.path += [os.path.dirname(os.path.dirname(os.path.dirname(__file__)))]
from scheduler import Scheduler
from notificator import Notificator
from notification import SendNotification
from eventer import Eventer
from flowerweb.config.init_config import Config

cron = "13/14/15/16/17/18/19/20/21/22/23 0/30 0"  # как часто проверяет событыия в базе

config_section = Config().setup().get('notificator')
telebot = config_section.get('telebot')
url = config_section.get('url')
id = config_section.get('recipient')

Eventer(SendNotification,
        id=id,
        telebot=telebot,
        url=url)

notificator = Notificator()
notificator.registrate_cron(cron)
notificator.registrate_event(Eventer.events)

for events in Scheduler(notificator):
    Scheduler.check_event_status()
    print(Scheduler.time)
    if Scheduler.run_events:
        for event in events:
            Eventer.run(event)
        Scheduler.ban_by_cron()
