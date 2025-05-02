class check_request:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        try:
            result = self.func(*args, **kwargs)

            if result is None:
                result = True
        except:
            result = False

        return result