from scenes.level import Level
from generation.tile import Tile
from scenes.director import Director
from generation.generator import BaseGenerator
from systems.resource_manager import ResourceManager, Resource
from generation.base_terrain import BaseTerrain, TerrainType

from noise import snoise2
import numpy as np
import pygame

from constants import TILE_SIZE

class CaveGenerator(BaseGenerator):
    def __init__(self, terrain):
        rmgr = ResourceManager.get_instance()
        self.floor_sprite = rmgr.load_tile(Resource.CAVE_FLOOR)

        self.wall_sprite_up = rmgr.load_tile(Resource.CAVE_WALL_UP)
        self.wall_sprite_down = rmgr.load_tile(Resource.CAVE_WALL_DOWN)
        self.wall_sprite_left = rmgr.load_tile(Resource.CAVE_WALL_LEFT)
        self.wall_sprite_right = rmgr.load_tile(Resource.CAVE_WALL_RIGHT)
        self.wall_sprite_leftup = rmgr.load_tile(Resource.CAVE_WALL_LEFTUP)
        self.wall_sprite_rightup = rmgr.load_tile(Resource.CAVE_WALL_RIGHTUP)
        self.wall_sprite_leftdown = rmgr.load_tile(Resource.CAVE_WALL_LEFTDOWN)
        self.wall_sprite_rightdown = rmgr.load_tile(Resource.CAVE_WALL_RIGHTDOWN)
        self.wall_sprite_innerleftup = rmgr.load_tile(Resource.CAVE_WALL_INNERLEFTUP)
        self.wall_sprite_innerrightup = rmgr.load_tile(Resource.CAVE_WALL_INNERRIGHTUP)
        self.wall_sprite_innerleftdown = rmgr.load_tile(Resource.CAVE_WALL_INNERLEFTDOWN)
        self.wall_sprite_innerrightdown = rmgr.load_tile(Resource.CAVE_WALL_INNERRIGHTDOWN)

        super().__init__(
            (6.0, 6.0),
            (2, 2),
            terrain
        )

    def coordinate_transform(self, x, y):
        return (x + snoise2(x*10 + 2711, y*10 - 14144) * y/10, y + snoise2(x*10 + 6789, y*10 + 10001) * y/10)

    def get_sprite(self, x, y, surroundings):
        if surroundings[1, 1] == TerrainType.GROUND:
            return self.get_ground_sprite(x, y)
        
        return self.get_wall_sprite(x, y, surroundings)

    def get_wall_sprite(self, x, y, surroundings):
        if surroundings[2, 1] == TerrainType.GROUND:
            if surroundings[1, 2] == TerrainType.GROUND:
                return self.wall_sprite_leftup
            if surroundings[1, 0] == TerrainType.GROUND:
                return self.wall_sprite_rightup
            return self.wall_sprite_up
        
        if surroundings[0, 1] == TerrainType.GROUND:
            if surroundings[1, 2] == TerrainType.GROUND:
                return self.wall_sprite_leftdown
            if surroundings[1, 0] == TerrainType.GROUND:
                return self.wall_sprite_rightdown
            return self.wall_sprite_down
        
        if surroundings[1, 2] == TerrainType.GROUND:
            return self.wall_sprite_left
        
        if surroundings[1, 0] == TerrainType.GROUND:
            return self.wall_sprite_right
        
        if surroundings[0, 0] == TerrainType.GROUND:
            return self.wall_sprite_innerrightdown
        if surroundings[0, 2] == TerrainType.GROUND:
            return self.wall_sprite_innerleftdown
        if surroundings[2, 0] == TerrainType.GROUND:
            return self.wall_sprite_innerrightup
        if surroundings[2, 2] == TerrainType.GROUND:
            return self.wall_sprite_innerleftup

        return None

    def get_ground_sprite(self, x, y):
        return self.floor_sprite
    
    def noise_wall_condition(self, n, x, y):
        x_dist = abs(x - 85) / 85
        y_dist = y / 170
        x_factor = n - x_dist
        return x_factor < y_dist - 1.0 or x_dist / 5.0 - 0.005 > y_dist**2

class CaveTerrain(BaseTerrain):
    def populate(self):
        self.data = np.full((171, 171), TerrainType.NONE, dtype=np.int16)
        self.height, self.width = self.data.shape
        self.starting_tiles = [(84, 3), (85, 3), (86, 3)]

        resource_manager = ResourceManager.get_instance()
        andesite_sprite = resource_manager.load_tile(Resource.POLISHED_ANDESITE)
        for x in range(85 - 1, 85 + 2):
            for y in range(0, 3):
                self.data[y, x] = TerrainType.GROUND
                self.sprites.add(Tile(x, y, andesite_sprite))

        self.player_starting_position = (TILE_SIZE * 85.5, TILE_SIZE * 1.5)

class CaveLevel(Level):
    def __init__(self):
        terrain = CaveTerrain()
        generator = CaveGenerator(terrain)
        background_color = (10, 0, 0)

        super().__init__(generator, terrain, background_color)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Director().switch_scene(CaveLevel())

        super().handle_events(events)