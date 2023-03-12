import pygame
from entities.living.player.player import Player
from gui.hud.hud import Hud
from mechanics.magic.magic_upgrade_system import MagicUpgradeSystem
from scenes.menus.pause_menu import PauseMenu
from scenes.menus.upgrade_menu import UpgradeMenu
from scenes.scene import Scene
from systems.camera_manager import CameraManager, ScrollableGroup


class Level(Scene):
    def __init__(self, generator, terrain, background_color):
        super().__init__()
        self.magic_upgrade_system = MagicUpgradeSystem.get_instance()
        self.bullet_group = ScrollableGroup()

        player_model = self.game_model.get_player()
        self.player = Player.from_player_model(player_model, (0, 0))

        self.generator = generator
        self.terrain = terrain
        self.background_color = background_color

        self.player_group = ScrollableGroup(self.player)

        self.camera_mgr = CameraManager.get_instance()
        self.camera_mgr.set_center(self.player.get_position())

        self.animation_group = ScrollableGroup()
        self.enemy_group = ScrollableGroup()
        self.enemy_bullets = ScrollableGroup()

        self.hud = Hud()

    def setup(self):
        self.generator.generate()
        self.player.set_position(self.terrain.get_player_starting_position())
        self.player.setup(self.bullet_group, self.__player_level_up)
        self.hud.setup(self)

    def __player_level_up(self):
        def apply_upgrade(upgrade):
            self.magic_upgrade_system.pick_upgrade(upgrade)
            self.player.apply_magical_upgrade(upgrade)

        possible_upgrades = self.magic_upgrade_system.get_random_upgrades(3)
        upgrades = [upgrade for upgrade in possible_upgrades if upgrade is not None]

        self.director.push_scene(UpgradeMenu(upgrades, apply_upgrade))

    def update(self, elapsed_time):
        # Update camera
        self.camera_mgr.update(elapsed_time)

        self.player.update(elapsed_time)
        self.bullet_group.update(elapsed_time)
        self.animation_group.update(elapsed_time)
        self.__check_bullet_colision()
        self.__check_bullet_enemy_collision()
        self.__check_enemy_bullet_with_player_colision()

    def __check_bullet_colision(self):

        # as we take into account if the bullet is or not on the ground,
        # it is not neccessary to check bullet's previous position to avoid
        # wall noclip. The latter one would happen if the bullet's speed is greater
        # than wall's width, and if we only took into account wall collision
        for bullet in self.bullet_group:
            if not self.terrain.on_ground(bullet.rect):
                bullet.collide(self.animation_group.add)

    def __check_bullet_enemy_collision(self):
        for bullet in self.bullet_group:
            for enemy in self.enemy_group:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.hit(bullet.damage, bullet.direction * 10.0)
                    bullet.kill()
                    break

    def __check_enemy_bullet_with_player_colision(self):
        for bullet in self.enemy_bullets:
            if bullet.rect.colliderect(self.player.rect):
                self.player.hit(bullet.damage, bullet.direction * 10.0)
                bullet.kill()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.director.push_scene(PauseMenu())

    def draw(self, screen):
        screen.fill(self.background_color)
        self.terrain.draw(screen)
        self.player_group.draw(screen)
        self.enemy_group.draw(screen)
        self.bullet_group.draw(screen)
        self.animation_group.draw(screen)
        self.hud.draw(screen)

    def pop_back(self):
        pass

    def get_terrain(self):
        return self.terrain

    def get_player(self):
        return self.player

    def spawn_enemy(self, enemy):
        enemy.setup(self.enemy_bullets)
        self.enemy_group.add(enemy)
        enemy.observable_pos.add_listener(self.hud.minimap)
