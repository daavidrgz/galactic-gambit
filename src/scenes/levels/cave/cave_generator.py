from generation.base_terrain import TerrainType
from generation.base_generator import BaseGenerator
from systems.resource_manager import Resource, ResourceManager
from noise import snoise2


class CaveGenerator(BaseGenerator):
    def __init__(self, terrain):
        rmgr = ResourceManager.get_instance()
        self.floor_sprite = rmgr.load_tile(Resource.CAVE_FLOOR)

        self.wall_spr_up = rmgr.load_tile(Resource.CAVE_WALL_UP)
        self.wall_spr_down = rmgr.load_tile(Resource.CAVE_WALL_DOWN)
        self.wall_spr_left = rmgr.load_tile(Resource.CAVE_WALL_LEFT)
        self.wall_spr_right = rmgr.load_tile(Resource.CAVE_WALL_RIGHT)
        self.wall_spr_leftup = rmgr.load_tile(Resource.CAVE_WALL_LEFTUP)
        self.wall_spr_rightup = rmgr.load_tile(Resource.CAVE_WALL_RIGHTUP)
        self.wall_spr_leftdown = rmgr.load_tile(Resource.CAVE_WALL_LEFTDOWN)
        self.wall_spr_rightdown = rmgr.load_tile(Resource.CAVE_WALL_RIGHTDOWN)
        self.wall_spr_inleftup = rmgr.load_tile(Resource.CAVE_WALL_INNERLEFTUP)
        self.wall_spr_inrightup = rmgr.load_tile(Resource.CAVE_WALL_INNERRIGHTUP)
        self.wall_spr_inleftdown = rmgr.load_tile( Resource.CAVE_WALL_INNERLEFTDOWN)
        self.wall_spr_inrightdown = rmgr.load_tile(Resource.CAVE_WALL_INNERRIGHTDOWN)

        super().__init__((6.0, 6.0), (2, 2), terrain, (7000, 20000))

    # Warp noise sampling coordinates with noise. Noise influence is determined by Y
    # coordinate -> deeper down = more distortion
    def coordinate_transform(self, x, y):
        return (
            x + snoise2(x * 10 + 2711, y * 10 - 14144) * y / 10,
            y + snoise2(x * 10 + 6789, y * 10 + 10001) * y / 10,
        )

    def get_sprite(self, x, y, surroundings):
        if surroundings[1, 1] == TerrainType.GROUND:
            return self.get_ground_sprite(x, y)

        return self.get_wall_sprite(x, y, surroundings)

    # Decide wall countour shape
    def get_wall_sprite(self, x, y, surroundings):
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

    def get_ground_sprite(self, x, y):
        return self.floor_sprite

    # Further from the center horizontally, as well as further down vertically, walls are more likely.
    # A quadratic curve defines the entrance to the cave
    def noise_wall_condition(self, n, x, y):
        x_dist = abs(x - 85) / 85
        y_dist = y / 170
        x_factor = n - x_dist
        return x_factor < y_dist - 1.0 or x_dist / 5.0 - 0.008 > y_dist**2

    # Distance as a combination of position and depth
    def distance_function(self, x0, y0, x1, y1, depth):
        return abs(x0 - x1) / 6 - abs(y0 - y1) + depth * 2
