from scenes.scene_manager import scene_manager


class Scene:
    def __init__(self):
        self.scene_manager = scene_manager

    def draw(self, screen):
        raise NotImplementedError

    def update(self, elapsed_time):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError
