from animations.animated_sprite import AnimatedSprite
from entities.misc.chest_entity import ChestEntity
from entities.living.player.player import Player
from systems.magic_upgrade_system import MagicUpgradeSystem
from systems.tech_upgrade_system import TechUpgradeSystem
from scenes.levels.groups import EnemyGroup, ParallaxGroup, ScrollableGroup
from scenes.menus.game_over_menu import GameOverMenu
from scenes.menus.upgrade_menu import UpgradeMenu
from scenes.menus.pause_menu import PauseMenu
from scenes.transition import Transition
from scenes.scene import Scene
from systems.rng_system import Generator, RngSystem
from generation.enemy_spawning import spawn_enemies
from utils.math import manhattan_norm, square_norm
from gui.hud.hud import Hud

import pygame
import numpy as np
from itertools import chain

from constants.game_constants import (
    TILE_SIZE,
    BACKGROUND_DIMMING,
    DESIGN_WIDTH,
    DESIGN_HEIGHT,
)


class Level(Scene):
    def __init__(
        self,
        generator,
        terrain,
        scene_music,
        player_footsteps,
        background=None,
    ):
        super().__init__()
        self.magic_upgrade_system = MagicUpgradeSystem.get_instance()
        self.tech_upgrade_system = TechUpgradeSystem.get_instance()

        self.generator = generator
        self.terrain = terrain
        self.background = background
        self.scene_music = scene_music
        self.player_footsteps = player_footsteps

        player_model = self.game_model.get_player()
        self.player = Player.from_player_model(player_model, (0, 0))

        self.player_group = ScrollableGroup(self.player)
        self.animation_group = ScrollableGroup()
        self.enemy_group = EnemyGroup()
        self.player_bullets = ScrollableGroup()
        self.enemy_bullets = ScrollableGroup()

        self.parallax_rate = 0.2
        self.background_group = ParallaxGroup((self.parallax_rate, self.parallax_rate))

        self.misc_entities = ScrollableGroup()
        self.draw_ordered = ScrollableGroup()

        self.hud = Hud()

    def load(self):
        self.generator.generate()
        self.__spawn_chest_entity()

        self.hud.setup(self)

        spawn_enemies(
            self, self.terrain, self.possible_enemy_spawns, self.enemy_spawn_level
        )

        if self.background:
            self.__setup_bg()

        super().load()

    def setup(self):
        if not self.load_completed:
            self.load()

        self.player.position = self.terrain.player_starting_position
        self.player.setup(
            level=self,
            on_level_up=self.player_magic_upgrade,
            on_death=self.__player_death,
        )

        self.enemy_group.add_listener(self.terrain)

        super().setup()

    def __setup_bg(self):
        terrain_size = np.array((self.terrain.width, self.terrain.height)) * TILE_SIZE
        middle_terrain_pos = terrain_size // 2
        background_image = self.resource_manager.load_image(self.background)

        bg_veil = pygame.Surface(background_image.get_size())
        bg_veil.set_alpha(BACKGROUND_DIMMING)
        background_image.blit(bg_veil, bg_veil.get_rect())

        bg_width, bg_height = background_image.get_size()
        size_ratio = max(
            (DESIGN_WIDTH + terrain_size[0] * self.parallax_rate) / bg_width,
            (DESIGN_HEIGHT + terrain_size[1] * self.parallax_rate) / bg_height,
        )

        bg_width *= size_ratio
        bg_height *= size_ratio
        background_image = pygame.transform.scale(
            background_image, (bg_width, bg_height)
        )

        # In order to simulate parallax background on the middle of the map,
        # we must multiply the position with the parallax rate,
        # so it seems to be 'centered' with the parallax 1.0
        middle_terrain_pos = middle_terrain_pos * self.parallax_rate
        background_sprite = AnimatedSprite(
            background_image,
            middle_terrain_pos + np.array((DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2)),
        )
        self.background_group.add(background_sprite)

    def __spawn_chest_entity(self):
        rng = RngSystem().get_rng(Generator.MAP)
        sx, sy = self.terrain.player_starting_position
        sx //= TILE_SIZE
        sy //= TILE_SIZE

        ex, ey = self.terrain.end_position
        ex //= TILE_SIZE
        ey //= TILE_SIZE

        min_distance = 100
        while True:
            x = rng.randrange(self.terrain.width)
            y = rng.randrange(self.terrain.height)

            if not self.terrain.on_ground_area((range(x, x + 2), range(y, y + 2))):
                continue

            if (
                min(manhattan_norm((x - sx, y - sy)), manhattan_norm((x - ex, y - ey)))
                < min_distance
            ):
                min_distance -= 1
                continue

            break

        self.chest_position = ((x + 1) * TILE_SIZE, (y + 1) * TILE_SIZE)
        self.spawn_misc_entity(ChestEntity(self.chest_position))

    def __player_death(self):
        self.game_model.delete_save()
        self.director.switch_scene(Transition(GameOverMenu()))

    def player_magic_upgrade(self):
        def apply_upgrade(upgrade):
            self.magic_upgrade_system.pick_upgrade(upgrade)
            self.player.apply_magical_upgrade(upgrade)

        possible_upgrades = self.magic_upgrade_system.get_random_upgrades(3)
        upgrades = [upgrade for upgrade in possible_upgrades if upgrade is not None]

        self.director.push_scene(UpgradeMenu(upgrades, apply_upgrade))

    def player_tech_upgrade(self):
        def apply_upgrade(upgrade):
            self.tech_upgrade_system.pick_upgrade(upgrade)
            self.player.apply_tech_upgrade(upgrade)

        possible_upgrades = self.tech_upgrade_system.get_random_upgrades(3)
        upgrades = [upgrade for upgrade in possible_upgrades if upgrade is not None]

        self.director.push_scene(UpgradeMenu(upgrades, apply_upgrade))

    def __check_player_reached_end(self):
        if self.enemy_group.get_num_enemies() > 0:
            return

        distance_sqr = square_norm(self.player.position - self.terrain.end_position)
        if distance_sqr < (3 * TILE_SIZE) ** 2:
            self.game_model.update_player(self.player)
            self.game_model.level = self.next_level
            self.game_model.save()
            self.director.switch_scene(Transition(self.next_level()))

    def update(self, elapsed_time):
        # Check level end condition
        self.__check_player_reached_end()
        # Update camera
        self.camera_mgr.update(elapsed_time)

        self.player.update(elapsed_time)
        self.enemy_group.update(elapsed_time)
        self.player_bullets.update(elapsed_time)
        self.enemy_bullets.update(elapsed_time)
        self.animation_group.update(elapsed_time)
        self.misc_entities.update(elapsed_time)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.director.push_scene(PauseMenu())

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.background_group.draw(screen)
        self.terrain.draw(screen)

        self.__draw_ordered(screen)

        self.player_bullets.draw(screen)
        self.enemy_bullets.draw(screen)
        self.animation_group.draw(screen)
        self.hud.draw(screen)

    def __draw_ordered(self, screen):
        self.draw_ordered.empty()
        self.draw_ordered.add(
            sorted(
                chain(self.player_group, self.enemy_group, self.misc_entities),
                key=lambda a: a.rect.bottom,
            )
        )
        self.draw_ordered.draw(screen)

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
