from ai.base_ai import BaseAI, AIState
from systems.rng_system import RngSystem, Generator
from ai.algorithms import wander, find_path, search_player
from utils.math import rotate_vector

import numpy as np

from constants.game_constants import TILE_SIZE


class RangedAI(BaseAI):
    def __init__(self, vision_range, tracking_range, attack_range, melee_range):
        super().__init__()
        self.rng = RngSystem().get_rng(Generator.ENEMIES)

        self.vision_range = vision_range
        self.tracking_range = tracking_range
        self.attack_range = attack_range
        self.melee_range = melee_range
        self.attack_timer = 0
        self.previous_direction = None
        self.angle_deviation = None
        self.wander_timer = None
        self.wandering = False

        self.desired_distance = (
            self.melee_range + (self.attack_range - self.melee_range) / 2
        )

        self.actions[AIState.IDLE] = self.idle
        self.actions[AIState.PREPARING] = self.prepare
        self.actions[AIState.ATTACKING] = self.attack
        self.actions[AIState.ALERT] = self.alert

    def idle(self, enemy, player, terrain, elapsed_time):
        # Compute distance to player, if the player is in vision range
        # and there's direct line of sight change to PREPARING state
        player_pos = player.position
        enemy_pos = enemy.position

        if search_player(enemy_pos, player_pos, terrain, self.vision_range):
            self.state = AIState.PREPARING
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

    def prepare(self, enemy, player, terrain, elapsed_time):
        # If we haven't decided a direction from which to attack
        if self.angle_deviation is None:
            self.angle_deviation = self.rng.random() * 30 - 15

        objective_pos = player.position.copy()
        enemy_pos = enemy.position
        ray = enemy_pos - objective_pos
        ray *= self.desired_distance / np.linalg.norm(ray)
        attack_from = rotate_vector(ray, self.angle_deviation)
        for _ in range(360 // 15):
            if search_player(
                objective_pos + attack_from, objective_pos, terrain, np.inf, 50
            ):
                break
            attack_from = rotate_vector(attack_from, 15)

        # Compute distance to player, if out of tracking range change to ALERT
        # and if in melee range change to ATTACK state
        objective_pos += attack_from

        diff_vector = objective_pos - enemy_pos

        distance = np.linalg.norm(diff_vector)
        if distance <= 2 * TILE_SIZE:
            self.state = AIState.ATTACKING
            return
        # if distance > self.tracking_range:
        #    self.state = AIState.ALERT
        #    return

        # Track player and avoid walls
        self.previous_direction = find_path(
            enemy_pos, diff_vector, distance, self.previous_direction, terrain
        )

        enemy.set_target(enemy_pos + self.previous_direction)

    def attack(self, enemy, player, terrain, elapsed_time):
        # If distance inside attack range and > melee range attack
        # If distance inside attack range and < melee range PREPARING
        # If distance > attack range PREPARING
        # If no line of sight PREPARING
        # Compute distance to player, if in attack range attack
        # else change back to PREPARING state
        player_pos = player.position
        enemy_pos = enemy.position

        diff_vector = player_pos - enemy_pos

        distance = np.linalg.norm(diff_vector)
        if distance < self.melee_range:
            self.state = AIState.PREPARING
            self.previous_direction = None
            self.attack_from = None
            return
        if distance > self.attack_range:
            self.state = AIState.PREPARING
            self.previous_direction = None
            self.attack_from = None

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
            self.state = AIState.PREPARING
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
