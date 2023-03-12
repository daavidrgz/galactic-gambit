from constants.game_constants import DESIGN_HEIGHT
from gui.hud.hud_element import HudElement
from systems.resource_manager import Resource
from utils.observer import Observer


class EnemyCounter(HudElement, Observer):
    def __init__(self):
        super().__init__()
        self.font = self.resource_manager.load_font(Resource.FONT_MD)

    def setup(self, **kwargs):
        enemies = kwargs["enemies"]
        enemies.add_listener(self)
        self.__update_counter(enemies)

    def draw(self, screen):
        screen.blit(self.counter, (20, DESIGN_HEIGHT - self.counter.get_height() - 40))

    def __update_counter(self, enemies):
        self.counter = self.font.render(
            f"Enemies alive: {enemies.get_num_enemies()}", True, (255, 255, 255)
        )

    def notify(self, enemies):
        self.__update_counter(enemies)
