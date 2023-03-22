from utils.observer import Observer
from gui.hud.hud_element import HudElement
from systems.resource_manager import Resource, ResourceManager

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
        self.chest_marker = ResourceManager().load_image(Resource.CHEST_MINI)
        self.chest_marker = pygame.transform.scale(
            self.chest_marker, [x * 2 for x in self.chest_marker.get_size()]
        )

        self.enemy_positions = dict()

    def setup(self, **kwargs):
        self.map_buffer = kwargs["map_buffer"]

        self.terrain_size = kwargs["terrain_size"]
        self.scaling_factor = (
            MINIMAP_SIZE / (TILE_SIZE * self.terrain_size[0]),
            MINIMAP_SIZE / (TILE_SIZE * self.terrain_size[1]),
        )

        self.chest_position_x = kwargs["chest_position"][0] * self.scaling_factor[0]
        self.chest_position_y = kwargs["chest_position"][1] * self.scaling_factor[1]

        player = kwargs["player"]
        self.player_id = player.get_id()
        self.__set_entity_pos(self.player_id, player.position)
        player.observable_pos.add_listener(self)

    def draw(self, screen):
        w, h = screen.get_size()
        w -= 10
        h -= 10
        start_x = w - MINIMAP_SIZE
        start_y = h - MINIMAP_SIZE
        screen.blit(self.map_buffer, (start_x, start_y, w, h))

        for id in self.enemy_positions:
            self.__draw_enemy(screen, id, start_x, start_y)

        self.__draw_chest(screen, start_x, start_y)
        self.__draw_player(screen, start_x, start_y)

    def __draw_player(self, screen, start_x, start_y):
        screen.blit(
            self.player_marker,
            (
                start_x + self.player_x - 1,
                start_y + self.player_y - 1,
                start_x + self.player_x + 2,
                start_y + self.player_y + 2,
            ),
        )

    def __draw_enemy(self, screen, enemy_id, start_x, start_y):
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

    def __draw_chest(self, screen, start_x, start_y):
        screen.blit(
            self.chest_marker,
            (
                start_x + self.chest_position_x - 3,
                start_y + self.chest_position_y - 3,
            ),
        )

    def __set_entity_pos(self, id, position):
        x = position[0] * self.scaling_factor[0]
        y = position[1] * self.scaling_factor[1]

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

        self.__set_entity_pos(id, position)
