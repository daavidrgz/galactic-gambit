from utils.observer import Observer
from gui.hud.hud_element import HudElement

import pygame

from constants.gui_constants import MINIMAP_SIZE

class Minimap(HudElement, Observer):
    def __init__(self):
        super().__init__()

    def setup(self, **kwargs):
        self.map_buffer = kwargs['map_buffer']

    def draw(self, screen):
        w, h = screen.get_size()
        w -= 10
        h -= 10
        screen.blit(
            self.map_buffer,
            (w-MINIMAP_SIZE, h-MINIMAP_SIZE, w, h)
        )
        # marker = pygame.Surface((4,4))
        # marker.fill((0,255,0))
        # x, y = Director().get_scene().get_player().get_position()
        # x = x * 256 // (TILE_SIZE * self.width)
        # y = y * 256 // (TILE_SIZE * self.height)
        # screen.blit(marker, (x-1,y-1,x+2,y+2))

    def notify(self, magic_level):
        pass