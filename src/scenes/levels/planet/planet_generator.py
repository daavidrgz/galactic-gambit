import numpy as np
from generation.base_terrain import TerrainType
from generation.base_generator import BaseGenerator
from systems.resource_manager import Resource, ResourceManager


class PlanetGenerator(BaseGenerator):
    def __init__(self, terrain):
        super().__init__((10, 10), (2, 2), terrain, (5500, 10000))

        rmgr = ResourceManager.get_instance()
        self.floor_sprite = rmgr.load_tile(Resource.PLANET_FLOOR)
        self.floor_spriteD1 = rmgr.load_tile(Resource.PLANET_FLOOR_D1)

        self.wall_spr_up = rmgr.load_tile(Resource.PLANET_WALL_UP)
        self.wall_spr_down = rmgr.load_tile(Resource.PLANET_WALL_DOWN)
        self.wall_spr_left = rmgr.load_tile(Resource.PLANET_WALL_LEFT)
        self.wall_spr_right = rmgr.load_tile(Resource.PLANET_WALL_RIGHT)
        self.wall_spr_leftup = rmgr.load_tile(Resource.PLANET_WALL_LEFTUP)
        self.wall_spr_rightup = rmgr.load_tile(Resource.PLANET_WALL_RIGHTUP)
        self.wall_spr_leftdown = rmgr.load_tile(Resource.PLANET_WALL_LEFTDOWN)
        self.wall_spr_rightdown = rmgr.load_tile(Resource.PLANET_WALL_RIGHTDOWN)
        self.wall_spr_inleftup = rmgr.load_tile(Resource.PLANET_WALL_INNERLEFTUP)
        self.wall_spr_inrightup = rmgr.load_tile(Resource.PLANET_WALL_INNERRIGHTUP)
        self.wall_spr_inleftdown = rmgr.load_tile(Resource.PLANET_WALL_INNERLEFTDOWN)
        self.wall_spr_inrightdown = rmgr.load_tile(Resource.PLANET_WALL_INNERRIGHTDOWN)

        # Get a noise offset based on seed for visual tile variation
        self.var_offset_x, self.var_offset_y = (
            (self.rng.random() - 0.5) * 1000000,
            (self.rng.random() - 0.5) * 1000000,
        )

    # Use polar coordinates for noise to cause ring-shaped levels
    def coordinate_transform(self, x, y):
        x -= 85
        y -= 85
        return (np.sqrt(x * x + y * y), np.arctan2(y, x) * 5)

    def get_sprite(self, x, y, surroundings):
        if surroundings[1, 1] == TerrainType.GROUND:
            return self.get_ground_sprite(x, y)

        return self.get_wall_spr(x, y, surroundings)

    # Decide wall countour shape
    def get_wall_spr(self, x, y, surroundings):
        if surroundings[2, 1] == TerrainType.GROUND:
            if surroundings[1, 2] == TerrainType.GROUND:
                return self.wall_spr_leftup
            if surroundings[1, 0] == TerrainType.GROUND:
                return self.wall_spr_rightup
            return self.wall_spr_up

        if surroundings[0, 1] == TerrainType.GROUND:
            if surroundings[1, 2] == TerrainType.GROUND:
                return self.wall_spr_leftdown
            if surroundings[1, 0] == TerrainType.GROUND:
                return self.wall_spr_rightdown
            return self.wall_spr_down

        if surroundings[1, 2] == TerrainType.GROUND:
            return self.wall_spr_left

        if surroundings[1, 0] == TerrainType.GROUND:
            return self.wall_spr_right

        if surroundings[0, 0] == TerrainType.GROUND:
            return self.wall_spr_inrightdown
        if surroundings[0, 2] == TerrainType.GROUND:
            return self.wall_spr_inleftdown
        if surroundings[2, 0] == TerrainType.GROUND:
            return self.wall_spr_inrightup
        if surroundings[2, 2] == TerrainType.GROUND:
            return self.wall_spr_inleftup

        return None

    # Ground gets random variations
    def get_ground_sprite(self, x, y):
        n = self.noise(x / 60 + self.var_offset_x, y / 60 + self.var_offset_y)

        if n > 0.70:
            return self.floor_spriteD1

        return self.floor_sprite

    # Walls are more likely the further we go from the center
    def noise_wall_condition(self, n, x, y):
        return n < (x / 114) ** 3

    # Merely use depth for distance on the planet level
    def distance_function(self, x0, y0, x1, y1, depth):
        return depth
