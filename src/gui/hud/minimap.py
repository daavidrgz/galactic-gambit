from utils.observer import Observer
from gui.hud.hud_element import HudElement

import pygame

from constants.game_constants import TILE_SIZE
from constants.gui_constants import MINIMAP_SIZE

class Minimap(HudElement, Observer):
    def __init__(self):
        super().__init__()

    def setup(self, **kwargs):
        self.map_buffer = kwargs['map_buffer']
        self.terrain_size = kwargs['terrain_size']

        player = kwargs['player']
        self.player_id = player.get_id()
        self.set_player_pos(player.get_position())
        player.observable_pos.add_listener(self)

    def draw(self, screen):
        w, h = screen.get_size()
        w -= 10
        h -= 10
        start_x = w - MINIMAP_SIZE
        start_y = h - MINIMAP_SIZE
        screen.blit(
            self.map_buffer,
            (start_x, start_y, w, h)
        )
        
        self.draw_player(screen, start_x, start_y)

    def draw_player(self, screen, start_x, start_y):
        marker = pygame.Surface((4,4))
        marker.fill((0,255,0))

        screen.blit(
            marker,
            (
                start_x + self.player_x - 1,
                start_y + self.player_y - 1,
                start_x + self.player_x + 2,
                start_y + self.player_y + 2
            )
        )

    def set_player_pos(self, position):
        self.player_x = position[0] * MINIMAP_SIZE // (TILE_SIZE * self.terrain_size[0])
        self.player_y = position[1] * MINIMAP_SIZE // (TILE_SIZE * self.terrain_size[1])

    def notify(self, id, position):
        if id == self.player_id:
            self.set_player_pos(position)