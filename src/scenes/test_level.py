from scenes.level import Level
from generation.terrain import Terrain
from generation.generator import BaseGenerator
from systems.resource_manager import ResourceManager
from systems.camera_manager import ScrollableGroup
from model.game_model import GameModel
from entities.living.player.player import Player

from constants import TILE_SIZE

import pygame
import numpy as np

class TestGenerator(BaseGenerator):
    def __init__(self, terrain):
        self.resource_manager = ResourceManager.get_instance()
        self.dirt_sprite = pygame.transform.scale(
            self.resource_manager.load_image(self.resource_manager.DIRT), (32, 32)
        )
        self.cobble_sprite = pygame.transform.scale(
            self.resource_manager.load_image(self.resource_manager.COBBLESTONE),
            (32, 32),
        )

        super().__init__(
            terrain,
            (10.0, 20.0),
            (7, 5),
        )

    def get_wall_sprite(self, x, y):
        new_tile = pygame.sprite.Sprite()
        new_tile.image = self.cobble_sprite
        new_tile.image_rect = new_tile.image.get_rect()
        new_tile.rect = new_tile.image.get_rect()
        new_tile.rect.centerx = x * TILE_SIZE + 16
        new_tile.rect.centery = y * TILE_SIZE + 16
        new_tile.x = new_tile.rect.centerx
        new_tile.y = new_tile.rect.centery
        return new_tile

    def get_ground_sprite(self, x, y):
        new_tile = pygame.sprite.Sprite()
        new_tile.image = self.dirt_sprite
        new_tile.image_rect = new_tile.image.get_rect()
        new_tile.rect = new_tile.image.get_rect()
        new_tile.rect.centerx = x * TILE_SIZE + 16
        new_tile.rect.centery = y * TILE_SIZE + 16
        new_tile.x = new_tile.rect.centerx
        new_tile.y = new_tile.rect.centery
        return new_tile

class TestLevel(Level):
    def __init__(self):
        self.bullet_group = ScrollableGroup() #TODO
        player_model = GameModel.get_instance().get_player()
        player = Player.from_player_model(
            player_model, (114 * TILE_SIZE, 114 * TILE_SIZE), self.bullet_group
        )

        terrain = Terrain(ScrollableGroup(), np.full((231, 231), False), (114, 114))
        generator = TestGenerator(terrain)

        super().__init__(generator, terrain, player, (0, 0, 0))