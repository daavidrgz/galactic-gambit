class Observable:
    def __init__(self):
        self.observers = []

    def add_listener(self, observer):
        self.observers.append(observer)

    def remove_listener(self, observer):
        self.observers.remove(observer)

    def notify_listeners(self, *args, **kwargs):
        for observer in self.observers:
            observer.notify(*args, **kwargs)
