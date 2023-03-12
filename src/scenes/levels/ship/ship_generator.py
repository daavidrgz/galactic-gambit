from generation.base_terrain import TerrainType
from generation.generator import BaseGenerator
from systems.resource_manager import Resource, ResourceManager


class ShipGenerator(BaseGenerator):
    def __init__(self, terrain):
        super().__init__((10, 20), (7, 5), terrain, (4500, 7000))

        rmgr = ResourceManager.get_instance()
        self.floor_sprite = rmgr.load_tile(Resource.SHIP_FLOOR)
        self.floor_spriteD1 = rmgr.load_tile(Resource.SHIP_FLOOR_D1)
        self.floor_spriteD2 = rmgr.load_tile(Resource.SHIP_FLOOR_D2)
        self.floor_spriteD3 = rmgr.load_tile(Resource.SHIP_FLOOR_D3)
        self.floor_spriteC1 = rmgr.load_tile(Resource.SHIP_FLOOR_C1)
        self.floor_spriteC2 = rmgr.load_tile(Resource.SHIP_FLOOR_C2)

        self.wall_sprite_up = rmgr.load_tile(Resource.SHIP_WALL_UP)
        self.wall_sprite_down = rmgr.load_tile(Resource.SHIP_WALL_DOWN)
        self.wall_sprite_left = rmgr.load_tile(Resource.SHIP_WALL_LEFT)
        self.wall_sprite_right = rmgr.load_tile(Resource.SHIP_WALL_RIGHT)
        self.wall_sprite_leftup = rmgr.load_tile(Resource.SHIP_WALL_LEFTUP)
        self.wall_sprite_rightup = rmgr.load_tile(Resource.SHIP_WALL_RIGHTUP)
        self.wall_sprite_leftdown = rmgr.load_tile(Resource.SHIP_WALL_LEFTDOWN)
        self.wall_sprite_rightdown = rmgr.load_tile(Resource.SHIP_WALL_RIGHTDOWN)
        self.wall_sprite_innerleftup = rmgr.load_tile(Resource.SHIP_WALL_INNERLEFTUP)
        self.wall_sprite_innerrightup = rmgr.load_tile(Resource.SHIP_WALL_INNERRIGHTUP)
        self.wall_sprite_innerleftdown = rmgr.load_tile(
            Resource.SHIP_WALL_INNERLEFTDOWN
        )
        self.wall_sprite_innerrightdown = rmgr.load_tile(
            Resource.SHIP_WALL_INNERRIGHTDOWN
        )

        self.var_offset_x, self.var_offset_y = (
            (self.rng.random() - 0.5) * 1000000,
            (self.rng.random() - 0.5) * 1000000,
        )

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
        n = self.noise(x / 10 + self.var_offset_x, y / 10 + self.var_offset_y)

        if n > 0.90:
            return self.floor_spriteD3
        if n > 0.75:
            return self.floor_spriteD2
        if n > 0.60:
            return self.floor_spriteD1

        if self.rng.random() > 0.995:
            return self.floor_spriteC1
        if self.rng.random() > 0.990:
            return self.floor_spriteC2

        return self.floor_sprite

    def noise_wall_condition(self, n, x, y):
        return n > 0.0
