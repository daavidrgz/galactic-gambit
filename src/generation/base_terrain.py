from generation.tile import Tile
from systems.camera_manager import CameraManager
from utils.observer import Observer
import utils.math
import utils.misc

from constants.game_constants import TILE_SIZE
from constants.gui_constants import MINIMAP_SIZE

from enum import IntEnum
import numpy as np
import pygame


class TerrainType(IntEnum):
    NONE = 0

    GROUND = 1
    WALL = 2

    GENERATING = -1
    BOUND = -2


class BaseTerrain(Observer):
    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.sprites_top = pygame.sprite.Group()
        self.buffer = None
        self.camera_mgr = CameraManager()

    def populate(self):
        raise NotImplementedError

    def place_end(self, end_coords):
        raise NotImplementedError

    def clear(self):
        self.sprites.empty()
        self.sprites_top.empty()
        self.data = None
        self.starting_tiles = None
        self.height = self.width = 0
        self.buffer = None

    def get_player_starting_position(self):
        return self.player_starting_position

    def get_end_position(self):
        return self.end_position

    def draw(self, screen):
        draw_area = self.buffer.get_rect().copy()
        scrollx, scrolly = self.camera_mgr.get_coords()
        draw_area.centerx -= round(scrollx)
        draw_area.centery -= round(scrolly)
        screen.blit(self.buffer, draw_area)

    def generate_buffer(self):
        self.buffer = pygame.Surface(
            (TILE_SIZE * self.width, TILE_SIZE * self.height), flags=pygame.SRCALPHA
        )
        self.sprites.draw(self.buffer)
        self.sprites_top.draw(self.buffer)

        self.minimap = pygame.transform.smoothscale(
            self.buffer, (MINIMAP_SIZE, MINIMAP_SIZE)
        )
        utils.misc.add_border(self.minimap, (0, 0, 0, 255))
        utils.misc.add_border(self.minimap, (255, 255, 255, 255))

    def get_minimap(self):
        return self.minimap

    def get_size(self):
        return (self.width, self.height)

    def on_ground(self, rect):
        starting_x, starting_y = rect.topleft
        rect_width, rect_height = rect.size
        end_x, end_y = starting_x + rect_width, starting_y + rect_height
        logical_starting_x, logical_starting_y = Tile.tile_to_logical_position(
            (starting_x, starting_y)
        )
        logical_end_x, logical_end_y = Tile.tile_to_logical_position((end_x, end_y))
        return (
            self.data[
                logical_starting_y : logical_end_y + 1,
                logical_starting_x : logical_end_x + 1,
            ]
            == TerrainType.GROUND
        ).all()

    def on_ground_point(self, point):
        x, y = Tile.tile_to_logical_position(point)
        return self.in_bounds(x, y) and self.data[y, x] == TerrainType.GROUND
    
    def on_ground_tile(self, tile):
        return self.in_bounds(tile[0], tile[1]) and self.data[tile[1], tile[0]] == TerrainType.GROUND

    def get_collision_vector(self, point, distance):
        tile_pos_x, tile_pos_y = Tile.tile_to_logical_position(point)
        tile_pos_x = int(tile_pos_x)
        tile_pos_y = int(tile_pos_y)
        pos = np.array(point, dtype=np.float64)
        for x in range(max(0, tile_pos_x - 1), min(self.width, tile_pos_x + 2)):
            for y in range(max(0, tile_pos_y - 1), min(self.height, tile_pos_y + 2)):
                if self.data[y, x] == TerrainType.GROUND:
                    continue
                r = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pos += utils.math.circle_rect_collision_vector(
                    (pos[0], pos[1], distance), r
                )
        return pos

    def in_bounds(self, x, y):
        return x >= 0 and y >= 0 and x < self.width and y < self.height

    def place_top_sprite(self, x, y, image):
        spr = pygame.sprite.Sprite()
        spr.image = image
        spr.rect = image.get_rect()
        spr.rect.topleft = (
            x * TILE_SIZE,
            y * TILE_SIZE,
        )
        self.sprites_top.add(spr)

    def open_ending(self):
        end_sprite = None
        for sprite in self.sprites_top:
            end_sprite = sprite
        if end_sprite is not None:
            self.buffer.blit(end_sprite.image, end_sprite.rect.topleft)

    def notify(self, enemies):
        enemy_amount = len(enemies)
        if enemy_amount < 1:
            self.open_ending()
