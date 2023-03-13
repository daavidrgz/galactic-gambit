from utils.observer import Observer
from gui.hud.hud_element import HudElement

import pygame

from constants.game_constants import TILE_SIZE
from constants.gui_constants import MINIMAP_SIZE


class Minimap(HudElement, Observer):
    def __init__(self):
        super().__init__()

        self.player_marker = pygame.Surface((4, 4))
        self.player_marker.fill((0, 255, 0))
        self.enemy_marker = pygame.Surface((3, 3))
        self.enemy_marker.fill((255, 0, 0))

        self.enemy_positions = dict()

    def setup(self, **kwargs):
        self.map_buffer = kwargs["map_buffer"]
        self.terrain_size = kwargs["terrain_size"]

        player = kwargs["player"]
        self.player_id = player.get_id()
        self.set_entity_pos(self.player_id, player.get_position())
        player.observable_pos.add_listener(self)

    def draw(self, screen):
        w, h = screen.get_size()
        w -= 10
        h -= 10
        start_x = w - MINIMAP_SIZE
        start_y = h - MINIMAP_SIZE
        screen.blit(self.map_buffer, (start_x, start_y, w, h))

        self.draw_player(screen, start_x, start_y)

        for id in self.enemy_positions:
            self.draw_enemy(screen, id, start_x, start_y)

    def draw_player(self, screen, start_x, start_y):
        screen.blit(
            self.player_marker,
            (
                start_x + self.player_x - 1,
                start_y + self.player_y - 1,
                start_x + self.player_x + 2,
                start_y + self.player_y + 2,
            ),
        )

    def draw_enemy(self, screen, enemy_id, start_x, start_y):
        try:
            x, y = self.enemy_positions[enemy_id]
        except KeyError:
            return

        screen.blit(
            self.enemy_marker,
            (
                start_x + x - 1,
                start_y + y - 1,
                start_x + x + 1,
                start_y + y + 1,
            ),
        )

    def set_entity_pos(self, id, position):
        x = position[0] * MINIMAP_SIZE // (TILE_SIZE * self.terrain_size[0])
        y = position[1] * MINIMAP_SIZE // (TILE_SIZE * self.terrain_size[1])

        if id == self.player_id:
            self.player_x = x
            self.player_y = y
            return

        self.enemy_positions[id] = (x, y)

    def notify(self, id, position):
        if position is None:
            if id == self.player_id:
                return
            self.enemy_positions.pop(id)
            return

        self.set_entity_pos(id, position)
