from systems.resource_manager import ResourceManager


class HudElement:
    def __init__(self):
        self.resource_manager = ResourceManager.get_instance()

    def setup(self, **kwargs):
        raise NotImplementedError

    def draw(self, screen):
        raise NotImplementedError
