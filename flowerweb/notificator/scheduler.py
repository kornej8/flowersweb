import time
from datetime import datetime


class Scheduler:
    time = None
    _events = []
    run_events = None
    _notificator = None
    run_once = None

    def __new__(cls, notificator):
        cls._notificator = notificator
        return Scheduler.run()

    def __init__(self, notificator):
        self.notificator = notificator

    @classmethod
    def run(cls):
        while True:
            time.sleep(1)
            _time = datetime.now()
            Scheduler.time = _time
            yield cls._notificator._events

    @staticmethod
    def get_match_by_cron_and_time(time, hour, min, sec):
        hour_match = int(time.strftime('%H')) in hour
        min_match = int(time.strftime('%M')) in min
        sec_match = int(time.strftime('%S')) in sec

        return hour_match and min_match and sec_match

    @classmethod
    def check_event_status(cls):
        hour = cls._notificator.rate.hour
        min = cls._notificator.rate.min
        sec = cls._notificator.rate.sec

        is_match = cls.get_match_by_cron_and_time(time=cls.time,
                                                  hour=hour,
                                                  min=min,
                                                  sec=sec)

        cls.run_events = is_match

    @classmethod
    def ban_by_cron(cls):
        cls.run_events = False
