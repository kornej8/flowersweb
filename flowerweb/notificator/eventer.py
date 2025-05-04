class Eventer:
    events = []

    def __init__(self, event, *args, **kwargs):
        self.events.append(event(*args, **kwargs))

    @classmethod
    def run(cls, event, *args, **kwargs):
        try:
            event(*args, **kwargs)
        except Exception as e:
            print(str(e))
