from entities.living.player.player import Player
from gui.hud import Hud
from mechanics.magic.magic_upgrade_system import MagicUpgradeSystem
from scenes.menus.pause_menu import PauseMenu
from scenes.menus.upgrade_menu import UpgradeMenu
from scenes.scene import Scene
from systems.camera_manager import CameraManager, ScrollableGroup
from systems.control_system import Action


class Level(Scene):
    def __init__(self, generator, terrain, background_color):
        super().__init__()
        self.magic_upgrade_system = MagicUpgradeSystem.get_instance()
        self.bullet_group = ScrollableGroup()

        player_model = self.game_model.get_player()
        self.player = Player.from_player_model(player_model, (0, 0), self.bullet_group)

        self.generator = generator
        self.terrain = terrain
        self.background_color = background_color

        self.player_group = ScrollableGroup(self.player)

        self.camera_mgr = CameraManager.get_instance()
        self.camera_mgr.set_center(self.player.get_position())

        self.animation_group = ScrollableGroup()
        self.enemy_group = ScrollableGroup()

        self.hud = Hud()

    def setup(self):
        self.generator.generate()
        self.player.set_position(self.terrain.get_player_starting_position())
        self.player.setup(self.__player_level_up)
        self.hud.setup(self.player)

    def update(self, elapsed_time):
        # Update camera
        self.camera_mgr.update(elapsed_time)

        self.player.update(elapsed_time)
        self.bullet_group.update(elapsed_time)
        self.animation_group.update(elapsed_time)
        self.__check_bullet_colission()

        if self.control_system.is_active_action(Action.PAUSE):
            self.director.push_scene(PauseMenu())

    def __player_level_up(self):
        upgrades = []
        for _ in range(3):
            upgrade = self.magic_upgrade_system.get_random_upgrade()
            if upgrade is None:
                break
            upgrades.append(upgrade)
        self.director.push_scene(
            UpgradeMenu(upgrades, self.player.apply_magical_upgrade)
        )

    def __check_bullet_colission(self):
        # as we take into account if the bullet is or not on the ground,
        # it is not neccessary to check bullet's previous position to avoid
        # wall noclip. The latter one would happen if the bullet's speed is greater
        # than wall's width, and if we only took into account wall collision
        for bullet in self.bullet_group:
            if not self.terrain.on_ground(bullet.rect):
                bullet.collide(self.animation_group)

    def handle_events(self, events):
        pass

    def draw(self, screen):
        screen.fill(self.background_color)
        self.terrain.draw(screen)
        self.player_group.draw(screen)
        self.enemy_group.draw(screen)
        self.bullet_group.draw(screen)
        self.animation_group.draw(screen)
        self.terrain.draw_minimap(screen)
        self.hud.draw(screen)

    def pop_back(self):
        pass

    def get_terrain(self):
        return self.terrain

    def get_player(self):
        return self.player
