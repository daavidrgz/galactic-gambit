from entities.living.player.player import Player
from generation.tile import Tile
from model.game_model import GameModel
from scenes.scene import Scene
from systems.camera_manager import CameraManager, ScrollableGroup


class Level(Scene):
    def __init__(self, generator, terrain, player_starting_position, background_color):

        self.bullet_group = ScrollableGroup()

        player_model = GameModel.get_instance().get_player()
        self.player = Player.from_player_model(
            player_model,
            Tile.get_tile_position(player_starting_position),
            self.bullet_group,
        )

        self.generator = generator
        self.terrain = terrain
        self.background_color = background_color

        self.player_group = ScrollableGroup(self.player)

        self.camera_mgr = CameraManager.get_instance()
        self.camera_mgr.set_center(self.player.get_position())

        super().__init__()

    def setup(self):
        self.player.setup()
        self.generator.generate()

    def update(self, elapsed_time):
        self.player.update(elapsed_time)
        self.bullet_group.update(elapsed_time)
        self.__check_bullet_colission()

    def __check_bullet_colission(self):
        # as we take into account if the bullet is or not on the ground,
        # it is not neccessary to check bullet's previous position to avoid
        # wall noclip. The latter one would happen if the bullet's speed is greater
        # than wall's width, and if we only took into account wall coliision
        for bullet in self.bullet_group:
            if not self.terrain.on_ground(bullet.rect):
                bullet.kill()

    def handle_events(self, events):
        pass

    def draw(self, screen):
        screen.fill(self.background_color)
        self.terrain.draw(screen)
        self.player_group.draw(screen)
        self.bullet_group.draw(screen)

    def pop_back(self):
        pass

    def get_terrain(self):
        return self.terrain
