from scenes.decorations.fade_scene import FadeInScene, FadeOutScene
from scenes.decorations.overlayed_scene import OverlayedScene


class SceneManager:
    def __init__(self):
        self.scenes = []

    def push_scene_raw(self, scene):
        self.scenes.append(scene)

    def pop_scene_raw(self):
        self.scenes.pop()

    def switch_scene_raw(self, scene):
        self.pop_scene_raw()
        self.push_scene_raw(scene)

    def push_scene(self, scene):
        previous_scene = None
        if len(self.scenes) > 0:
            previous_scene = self.get_current_scene()

        self.scenes.append(scene)
        self.scenes.append(FadeInScene(self, scene))

        if previous_scene is not None:
            self.scenes.append(FadeOutScene(self, previous_scene))

    def push_overlay(self, scene):
        background_scene = self.get_current_scene()
        overlayed_scene = OverlayedScene(self, background_scene, scene)
        self.push_scene_raw(overlayed_scene)

    def pop_scene(self):
        previous_scene = self.get_current_scene()
        self.pop_scene_raw()
        self.scenes.append(FadeInScene(self, self.get_current_scene()))
        self.scenes.append(FadeOutScene(self, previous_scene))

    def switch_scene(self, scene):
        previous_scene = self.get_current_scene()
        self.switch_scene_raw(scene)
        self.scenes.append(FadeInScene(self, scene))
        self.scenes.append(FadeOutScene(self, previous_scene))

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
