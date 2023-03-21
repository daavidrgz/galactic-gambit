from systems.game_model import GameModel
from scenes.director import Director
from systems.control_system import ControlSystem
from systems.resource_manager import ResourceManager
from systems.rng_system import RngSystem
from systems.sound_controller import SoundController


class Scene:
    def __init__(self):
        self.control_system = ControlSystem.get_instance()
        self.director = Director.get_instance()
        self.sound_controller = SoundController.get_instance()
        self.resource_manager = ResourceManager.get_instance()
        self.game_model = GameModel.get_instance()
        self.rng_system = RngSystem.get_instance()
        self.load_completed = False
        self.scene_music = None

    def load(self):
        self.load_completed = True

    def setup(self):
        if self.scene_music:
            self.sound_controller.play_music(self.scene_music)

    def update(self, elapsed_time):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError

    def draw(self, screen):
        raise NotImplementedError

    def pop_back(self):
        if self.scene_music:
            self.sound_controller.play_music(self.scene_music)
