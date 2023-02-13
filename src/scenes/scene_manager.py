class SceneManager:
    def __init__(self):
        self.scenes = []

    def push_scene_raw(self, scene):
        self.scenes.append(scene)

    def pop_scene_raw(self):
        self.scenes.pop()

    def switch_scene_raw(self, scene):
        self.scenes.pop()
        self.scenes.append(scene)

    def push_scene(self, scene):

        scene.fade_in()
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

        def callback():
            self.scenes.pop()
            self.scenes.append(scene)
            self.get_current_scene().fade_in()

        self.get_current_scene().hide_scene(callback)

    def get_current_scene(self):
        return self.scenes[-1]


# Make a singleton of SceneManager
# TODO: Make a singleton class
scene_manager = SceneManager()
