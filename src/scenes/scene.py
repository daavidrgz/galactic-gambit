from scenes.director import Director


class Scene:
    def __init__(self):
        self.director = Director.get_instance()

    def setup(self):
        raise NotImplementedError

    def update(self, elapsed_time):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError

    def draw(self, screen):
        raise NotImplementedError

    def pop_back(self):
        raise NotImplementedError
