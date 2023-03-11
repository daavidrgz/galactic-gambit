class Observer:
    def __init__(self):
        pass

    def notify(self, *args, **kwargs):
        raise NotImplementedError
