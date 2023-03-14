import numpy as np

from ai.base_ai import BaseAI, EnemyState
from systems.rng_system import RngSystem, Generator
from ai.algorithms import wander, find_path, search_player


class RangedAI(BaseAI):
    def __init__(self, vision_range, tracking_range, attack_range, melee_range):
        super().__init__()
        self.rng = RngSystem().get_rng(Generator.ENEMIES)

        self.vision_range = vision_range
        self.tracking_range = tracking_range
        self.attack_range = attack_range
        self.melee_range = melee_range
        self.previous_direction = None
        self.attack_from = None
        self.wander_timer = None
        self.wandering = False

        self.actions[EnemyState.IDLE] = self.idle
        self.actions[EnemyState.PREPARING] = self.preparing
        self.actions[EnemyState.ATTACKING] = self.attacking
        self.actions[EnemyState.ALERT] = self.alert

    def idle(self, enemy, player, terrain, elapsed_time):
        # Compute distance to player, if the player is in vision range
        # and there's direct line of sight change to PREPARING state
        player_pos = np.array(player.get_position(), dtype=np.float64)
        enemy_pos = np.array(enemy.get_position(), dtype=np.float64)

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
        # If distance > attack_range move to a point in between attack range and melee
        # range, find direct line of sight with player and change to ATTACKING
        # If distance > tracking_range change to ALERT
        ...

    def attacking(self, enemy, player, terrain, elapsed_time):
        # If distance inside attack range and > melee range attack
        # If distance inside attack range and < melee range PREPARING
        # If distance > attack range PREPARING
        # If no line of sight PREPARING
        ...

    def alert(self, enemy, player, terrain, elapsed_time):
        # Compute distance to player, if in tracking range change
        # to PREPARING state
        player_pos = np.array(player.get_position(), dtype=np.float64)
        enemy_pos = np.array(enemy.get_position(), dtype=np.float64)

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
