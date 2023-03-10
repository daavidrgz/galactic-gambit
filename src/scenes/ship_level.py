from scenes.level import Level
from scenes.director import Director
from generation.base_terrain import BaseTerrain, TerrainType
from generation.generator import BaseGenerator
from systems.resource_manager import ResourceManager
from systems.rng_system import RngSystem, Generator
from generation.tile import Tile

import numpy as np
import pygame

from constants import TILE_SIZE

class ShipGenerator(BaseGenerator):
    def __init__(self, terrain):
        super().__init__((10,20),(7,5),terrain)

        rmgr = ResourceManager.get_instance()
        self.floor_sprite = rmgr.load_tile(rmgr.SHIP_FLOOR)
        self.floor_spriteD1 = rmgr.load_tile(rmgr.SHIP_FLOOR_D1)
        self.floor_spriteD2 = rmgr.load_tile(rmgr.SHIP_FLOOR_D2)
        self.floor_spriteD3 = rmgr.load_tile(rmgr.SHIP_FLOOR_D3)
        self.floor_spriteC1 = rmgr.load_tile(rmgr.SHIP_FLOOR_C1)
        self.floor_spriteC2 = rmgr.load_tile(rmgr.SHIP_FLOOR_C2)
        self.cobble_sprite = rmgr.load_tile(rmgr.COBBLESTONE)

        self.var_offset_x, self.var_offset_y = (
            (self.rng.random() - 0.5) * 1000000,
            (self.rng.random() - 0.5) * 1000000,
        )

    def get_wall_sprite(self, x, y):
        return self.cobble_sprite

    def get_ground_sprite(self, x, y):
        n = self.noise(x / 10 + self.var_offset_x, y / 10 + self.var_offset_y)
        
        if n > 0.90: return self.floor_spriteD3
        if n > 0.75: return self.floor_spriteD2
        if n > 0.60: return self.floor_spriteD1

        if self.rng.random() > 0.995: return self.floor_spriteC1
        if self.rng.random() > 0.990: return self.floor_spriteC2

        return self.floor_sprite
    
    def noise_wall_condition(self, n, x, y):
        return n > 0.0

class ShipTerrain(BaseTerrain):
    def populate(self):
        data = np.full((148, 152), TerrainType.NONE, dtype=np.int16)
        self.data = np.pad(data, ((1,1),(1,1)), mode="constant", constant_values=TerrainType.BOUND)
        self.height, self.width = self.data.shape

        rng = RngSystem().get_rng(Generator.MAP)
        start_room_x = rng.randint(1, 154 // 7 - 1)

        resource_manager = ResourceManager.get_instance()
        andesite_sprite = resource_manager.load_tile(resource_manager.POLISHED_ANDESITE)
        cobble_sprite = resource_manager.load_tile(resource_manager.COBBLESTONE)
        for x in range(start_room_x * 7, start_room_x * 7 + 7):
            for y in range(150 - 10, 150 - 5):
                self.data[y, x] = TerrainType.GROUND
                self.sprites.add(Tile(x, y, andesite_sprite))

        for x in range(start_room_x * 7 - 1, start_room_x * 7 + 8):
            for y in [150 - 11, 150 - 5]:
                self.data[y, x] = TerrainType.WALL
                self.sprites.add(Tile(x, y, cobble_sprite))

        for y in range(150 - 10, 150 - 5):
            for x in [start_room_x * 7 - 1, start_room_x * 7 + 7]:
                self.data[y, x] = TerrainType.WALL
                self.sprites.add(Tile(x, y, cobble_sprite))

        for y in range(150 - 10, 150):
            for x in [start_room_x*7-3, start_room_x*7-2, start_room_x*7+8, start_room_x*7+9]:
                self.data[y, x] = TerrainType.BOUND

        for x in range(start_room_x * 7 - 1, start_room_x * 7 + 8):
            for y in range(150 - 4, 150):
                self.data[y, x] = TerrainType.BOUND

        self.player_starting_position = (TILE_SIZE * (start_room_x * 7 + 3.5), TILE_SIZE * (150 - 7.5))
        self.starting_tiles = [(start_room_x * 7 + 2, 150 - 11),(start_room_x * 7 + 3, 150 - 11),(start_room_x * 7 + 4, 150 - 11)]

class ShipLevel(Level):
    def __init__(self):
        terrain = ShipTerrain()
        generator = ShipGenerator(terrain)
        background_color = (0, 0, 0)
        super().__init__(generator, terrain, background_color)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Director().switch_scene(ShipLevel())

        super().handle_events(events)