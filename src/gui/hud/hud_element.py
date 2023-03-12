class HudElement():
    def __init__(self):
        pass

    def setup(self, **kwargs):
        raise NotImplementedError

    def draw(self, screen):
        raise NotImplementedError
