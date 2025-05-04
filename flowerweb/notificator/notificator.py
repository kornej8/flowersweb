class CronChecker:
    def __init__(self, cron):
        h, m, s = cron.split()
        self.hour = self.get_hours_list(h)
        self.min = self.get_mins_list(m)
        self.sec = self.get_secs_list(s)

    def decode_star(self, by: str):
        if by == 'hours':
            _range = range(0, 25)
        else:
            _range = range(0, 61)
        return [mu for mu in _range]

    def get_hours_list(self, hours: str):
        return self.mu_to_list(value=hours, by='hours')

    def get_mins_list(self, mins: str):
        return self.mu_to_list(value=mins, by='mins')

    def get_secs_list(self, secs: str):
        return self.mu_to_list(value=secs, by='secs')

    def mu_to_list(self, value: str, by: str):
        if value == '*':
            return self.decode_star(by=by)
        return list(map(lambda mu: int(mu.strip()), value.split('/')))


class Notificator:
    _range_checked = None
    _events = []

    def registrate_cron(self, cron):
        self.rate = CronChecker(cron)

    def registrate_event(self, event):
        self._events = event

    def check_time_range(self, scheduler):
        return scheduler.time
