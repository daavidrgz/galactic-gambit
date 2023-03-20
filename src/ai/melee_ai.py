from ai.base_ai import BaseAI, EnemyState
from ai.algorithms import wander, find_path, search_player
from systems.rng_system import RngSystem, Generator
from utils.math import rotate_vector

import numpy as np


class MeleeAI(BaseAI):
    def __init__(self, vision_range, tracking_range, melee_range):
        super().__init__()
        self.rng = RngSystem().get_rng(Generator.ENEMIES)

        self.vision_range = vision_range
        self.tracking_range = tracking_range
        self.melee_range = melee_range
        self.previous_direction = None
        self.attack_from = None
        self.wander_timer = None
        self.wandering = False

        self.actions[EnemyState.IDLE] = self.idle
        self.actions[EnemyState.PREPARING] = self.preparing
        self.actions[EnemyState.ATTACKING] = self.attack
        self.actions[EnemyState.ALERT] = self.alert

    def idle(self, enemy, player, terrain, elapsed_time):
        # Compute distance to player, if the player is in vision range
        # and there's direct line of sight change to PREPARING state
        player_pos = player.position
        enemy_pos = enemy.position

        if search_player(enemy_pos, player_pos, terrain, self.vision_range):
            self.state = EnemyState.PREPARING
            enemy.alerted()
            self.previous_direction = None
            self.attack_from = None
            return

        # Wander around
        new_target, self.wandering, self.wander_timer = wander(
            enemy_pos,
            enemy.get_target(),
            self.wandering,
            self.wander_timer,
            terrain,
            self.rng,
            elapsed_time,
            5000,
        )
        enemy.set_target(new_target)

    def preparing(self, enemy, player, terrain, elapsed_time):
        # If we haven't decided a direction from which to attack
        if self.attack_from is None:
            self.attack_from = rotate_vector(
                np.array((self.melee_range, 0.0)), self.rng.random() * 360
            )

        # Compute distance to player, if out of tracking range change to ALERT
        # and if in melee range change to ATTACK state
        player_pos = player.position + self.attack_from
        enemy_pos = enemy.position

        diff_vector = player_pos - enemy_pos

        distance = np.linalg.norm(diff_vector)
        if distance < self.melee_range:
            self.state = EnemyState.ATTACKING
            return
        if distance > self.tracking_range:
            self.state = EnemyState.ALERT
            return

        # Track player and avoid walls
        self.previous_direction = find_path(
            enemy_pos, diff_vector, distance, self.previous_direction, terrain
        )
        enemy.set_target(enemy_pos + self.previous_direction)

    def attack(self, enemy, player, terrain, elapsed_time):
        # Compute distance to player, if in attack range attack
        # else change back to PREPARING state
        player_pos = player.position
        enemy_pos = enemy.position

        diff_vector = player_pos - enemy_pos

        distance = np.linalg.norm(diff_vector)
        if distance > self.melee_range:
            self.state = EnemyState.PREPARING
            self.previous_direction = None
            self.attack_from = None
            return

        # Stop following the player
        enemy.set_target(None)

        # Attack player
        enemy.trigger_attack()

    def alert(self, enemy, player, terrain, elapsed_time):
        # Compute distance to player, if in tracking range change
        # to PREPARING state
        player_pos = player.position
        enemy_pos = enemy.position

        diff_vector = player_pos - enemy_pos

        distance = np.linalg.norm(diff_vector)
        if distance < self.tracking_range:
            self.state = EnemyState.PREPARING
            self.previous_direction = None
            self.attack_from = None
            return

        # Wander around
        new_target, self.wandering, self.wander_timer = wander(
            enemy_pos,
            enemy.get_target(),
            self.wandering,
            self.wander_timer,
            terrain,
            self.rng,
            elapsed_time,
            1000,
        )
        enemy.set_target(new_target)
