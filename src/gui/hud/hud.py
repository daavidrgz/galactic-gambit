from gui.hud.experience_bar import ExperienceBar
from gui.hud.minimap import Minimap

class Hud:
    def __init__(self):
        self.exp_bar = ExperienceBar()
        self.minimap = Minimap()

    def setup(self, level):
        self.exp_bar.setup(
            magic_level=level.get_player().magic_level,
        )
        self.minimap.setup(
            map_buffer=level.get_terrain().get_minimap(),
            terrain_size=level.get_terrain().get_size(),
            player=level.get_player(),
        )

    def draw(self, screen):
        self.exp_bar.draw(screen)
        self.minimap.draw(screen)
