class SceneManager:
    def __init__(self):
        self.scenes = []

    def push_scene(self, scene):
        if len(self.scenes) > 0:
            callback = lambda: self.scenes.append(scene)
            self.get_current_scene().hide_scene(callback)
        else:
            self.scenes.append(scene)

    def pop_scene(self):
        def callback():
            self.scenes.pop()
            self.get_current_scene().fade_in()

        self.get_current_scene().hide_scene(callback)

    def switch_scene(self, scene):
        self.pop_scene()
        self.push_scene(scene)

    def get_current_scene(self):
        return self.scenes[-1]

    def update_scene(self, elapsed_time):
        self.get_current_scene().update(elapsed_time)

    def draw_scene(self, screen):
        self.get_current_scene().draw(screen)

    def handle_events(self, events):
        self.get_current_scene().handle_events(events)


# Make a singleton of SceneManager
# TODO: Make a singleton class
scene_manager = SceneManager()
