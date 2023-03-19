from gui.hud.enemy_counter import EnemyCounter
from gui.hud.experience_bar import ExperienceBar
from gui.hud.health_bar import HealthBar
from gui.hud.minimap import Minimap


class Hud:
    def __init__(self):
        self.exp_bar = ExperienceBar()
        self.health_bar = HealthBar()
        self.minimap = Minimap()
        self.enemy_counter = EnemyCounter()

    def setup(self, level):
        self.exp_bar.setup(
            magic_level=level.get_player().magic_level,
        )
        self.minimap.setup(
            map_buffer=level.get_terrain().get_minimap(),
            terrain_size=level.get_terrain().get_size(),
            player=level.get_player(),
            chest_position=level.chest_position
        )
        self.health_bar.setup(hp=level.get_player().hp)
        self.enemy_counter.setup(enemies=level.enemy_group)

    def draw(self, screen):
        self.exp_bar.draw(screen)
        self.health_bar.draw(screen)
        self.minimap.draw(screen)
        self.enemy_counter.draw(screen)
