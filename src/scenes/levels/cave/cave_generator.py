from generation.base_terrain import TerrainType
from generation.generator import BaseGenerator
from systems.resource_manager import Resource, ResourceManager
from noise import snoise2


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
        self.wall_sprite_innerleftdown = rmgr.load_tile(
            Resource.CAVE_WALL_INNERLEFTDOWN
        )
        self.wall_sprite_innerrightdown = rmgr.load_tile(
            Resource.CAVE_WALL_INNERRIGHTDOWN
        )

        super().__init__((6.0, 6.0), (2, 2), terrain, (7000, 20000))

    def coordinate_transform(self, x, y):
        return (
            x + snoise2(x * 10 + 2711, y * 10 - 14144) * y / 10,
            y + snoise2(x * 10 + 6789, y * 10 + 10001) * y / 10,
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
        return self.floor_sprite

    def noise_wall_condition(self, n, x, y):
        x_dist = abs(x - 85) / 85
        y_dist = y / 170
        x_factor = n - x_dist
        return x_factor < y_dist - 1.0 or x_dist / 5.0 - 0.005 > y_dist**2

    def distance_function(self, x0, y0, x1, y1, depth):
        return abs(x0 - x1) + abs(y0 - y1) + depth
