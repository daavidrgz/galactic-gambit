from constants.game_constants import TILE_SIZE
from entities.living.player.player import Player
from gui.hud.hud import Hud
from mechanics.magic.magic_upgrade_system import MagicUpgradeSystem
from mechanics.technology.tech_upgrade_system import TechUpgradeSystem
from scenes.levels.groups import EnemyGroup, ScrollableGroup
from scenes.menus.game_over_menu import GameOverMenu
from scenes.menus.pause_menu import PauseMenu
from scenes.menus.upgrade_menu import UpgradeMenu
from scenes.scene import Scene
from scenes.transition import Transition
from systems.camera_manager import CameraManager

import pygame


class Level(Scene):
    def __init__(
        self,
        generator,
        terrain,
        background_color,
        scene_music,
        player_footsteps,
    ):
        super().__init__()
        self.magic_upgrade_system = MagicUpgradeSystem.get_instance()
        self.tech_upgrade_system = TechUpgradeSystem.get_instance()
        self.player_bullets = ScrollableGroup()

        player_model = self.game_model.get_player()
        self.player = Player.from_player_model(player_model, (0, 0))

        self.generator = generator
        self.terrain = terrain
        self.background_color = background_color

        self.player_group = ScrollableGroup(self.player)

        self.camera_mgr = CameraManager.get_instance()

        self.animation_group = ScrollableGroup()
        self.enemy_group = EnemyGroup()
        self.enemy_bullets = ScrollableGroup()

        self.misc_entities = ScrollableGroup()

        self.hud = Hud()
        self.scene_music = scene_music
        self.player_footsteps = player_footsteps

    def load(self):
        self.generator.generate()
        super().load()

    def setup(self):
        if not self.load_completed:
            self.load()

        self.player.set_position(self.terrain.get_player_starting_position())
        self.player.setup(
            level=self,
            on_level_up=self.__player_level_up,
            on_death=self.__player_death,
        )
        self.hud.setup(self)
        super().setup()

    def __player_death(self):
        self.game_model.delete_save()
        self.director.switch_scene(Transition(GameOverMenu()))

    def __player_level_up(self):
        def apply_upgrade(upgrade):
            self.magic_upgrade_system.pick_upgrade(upgrade)
            self.player.apply_magical_upgrade(upgrade)

        possible_upgrades = self.magic_upgrade_system.get_random_upgrades(3)
        upgrades = [upgrade for upgrade in possible_upgrades if upgrade is not None]

        self.director.push_scene(UpgradeMenu(upgrades, apply_upgrade))

    def __player_tech_upgrade(self):
        def apply_upgrade(upgrade):
            self.tech_upgrade_system.pick_upgrade(upgrade)
            self.player.apply_tech_upgrade(upgrade)

        possible_upgrades = self.tech_upgrade_system.get_random_upgrades(3)
        upgrades = [upgrade for upgrade in possible_upgrades if upgrade is not None]

        self.director.push_scene(UpgradeMenu(upgrades, apply_upgrade))

    def update(self, elapsed_time):
        # Check level end condition
        self.__check_player_reached_end()
        # Update camera
        self.camera_mgr.update(elapsed_time)

        self.player.update(elapsed_time)
        self.player_bullets.update(elapsed_time)
        self.enemy_bullets.update(elapsed_time)
        self.animation_group.update(elapsed_time)
        self.misc_entities.update(elapsed_time)

    def __check_player_reached_end(self):
        if self.enemy_group.get_num_enemies() > 0:
            return

        player_x, player_y = self.player.get_position()
        end_x, end_y = self.terrain.get_end_position()
        distance_sqr = (player_x - end_x) ** 2 + (player_y - end_y) ** 2
        if distance_sqr < (3 * TILE_SIZE) ** 2:
            self.game_model.update_player(self.player)
            self.game_model.level = self.next_level
            self.game_model.save()
            self.director.switch_scene(Transition(self.next_level()))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.director.push_scene(PauseMenu())
                if event.key == pygame.K_m:
                    self.__player_tech_upgrade()
                if event.key == pygame.K_n:
                    self.__player_level_up()
                if event.key == pygame.K_h:
                    self.player.hp.reduce(1)

    def draw(self, screen):
        screen.fill(self.background_color)
        self.terrain.draw(screen)
        self.player_group.draw(screen)
        self.enemy_group.draw(screen)
        self.misc_entities.draw(screen)
        self.player_bullets.draw(screen)
        self.enemy_bullets.draw(screen)
        self.animation_group.draw(screen)
        self.hud.draw(screen)

    def pop_back(self):
        super().pop_back()

    def get_terrain(self):
        return self.terrain

    def get_player(self):
        return self.player

    def spawn_enemy(self, enemy):
        # Add listener before setup, so observers gets first notification at setup
        enemy.observable_pos.add_listener(self.hud.minimap)
        enemy.setup(self)
        self.enemy_group.add(enemy)

    def spawn_misc_entity(self, entity):
        self.misc_entities.add(entity)
        entity.setup(self)

    def spawn_player_bullet(self, bullet):
        self.player_bullets.add(bullet)
        bullet.setup(self)

    def spawn_enemy_bullet(self, bullet):
        self.enemy_bullets.add(bullet)
        bullet.setup(self)
