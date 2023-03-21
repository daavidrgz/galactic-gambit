from constants.gui_constants import COLOR_BRIGHT
from utils.observer import Observer
from gui.hud.hud_element import HudElement
from systems.resource_manager import Resource
from systems.sound_controller import SoundController

from constants.game_constants import DESIGN_HEIGHT


class EnemyCounter(HudElement, Observer):
    def __init__(self):
        super().__init__()
        self.font = self.resource_manager.load_font(Resource.FONT_MD)

    def setup(self, **kwargs):
        enemies = kwargs["enemies"]
        enemies.add_listener(self)

    def draw(self, screen):
        screen.blit(self.counter, (20, DESIGN_HEIGHT - self.counter.get_height() - 40))

    def __update_counter(self, enemies):
        enemy_count = enemies.get_num_enemies()
        if enemy_count < 1:
            self.counter = self.font.render("Find the exit!", True, COLOR_BRIGHT)
            SoundController().play_sound(Resource.FINISH_LEVEL_SOUND)
            return

        self.counter = self.font.render(
            f"Remaining enemies: {enemy_count}", True, COLOR_BRIGHT
        )

    def notify(self, enemies):
        self.__update_counter(enemies)
