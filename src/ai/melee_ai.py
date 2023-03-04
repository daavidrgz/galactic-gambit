from ai.base_ai import BaseAI, EnemyState
from utils.singleton import Singleton

import numpy as np

class MeleeAI(BaseAI, metaclass=Singleton):
    def __init__(self, vision_range, tracking_range, melee_range):
        super().__init__()
        self.vision_range = vision_range
        self.tracking_range = tracking_range
        self.melee_range = melee_range
        
        self.actions[EnemyState.IDLE] = self.idle
        self.actions[EnemyState.PREPARING] = self.preparing
        self.actions[EnemyState.ATTACKING] = self.attack
        self.actions[EnemyState.ALERT] = self.alert
    
    def idle(self, enemy, player, terrain):
        # Compute distance to player, if the player is in vision range
        # and there's direct line of sight change to preparing state
        player_pos = np.array(player.get_position(), dtype=np.float64)
        enemy_pos = np.array(enemy.get_position(), dtype=np.float64)
        
        if self.search_player(enemy_pos, player_pos, terrain, self.vision_range):
            self.state = EnemyState.PREPARING
            return
        
        enemy.set_target(None)
        # TODO: If the distance to the player is too big or
        # there is no line of sight wander around
        
    def preparing(self, enemy, player, terrain):
        # Compute distance to player, if in tracking range keep preparing
        # and if in melee range change to attack state
        player_pos = np.array(player.get_position(), dtype=np.float64)
        enemy_pos = np.array(enemy.get_position(), dtype=np.float64)
        
        diff_vector = player_pos - enemy_pos

        distance = np.linalg.norm(diff_vector)
        if distance < self.melee_range:
            self.state = EnemyState.ATTACKING
            return
        if distance > self.tracking_range:
            self.state = EnemyState.ALERT
            return
        
        enemy.set_target(player_pos)
    
    def attack(self, enemy, player, terrain):
        # Compute distance to player, if in attack range attack 
        # else change back to preparing state
        player_pos = np.array(player.get_position(), dtype=np.float64)
        enemy_pos = np.array(enemy.get_position(), dtype=np.float64)
        
        diff_vector = player_pos - enemy_pos

        distance = np.linalg.norm(diff_vector)
        if distance > self.melee_range:
            self.state = EnemyState.PREPARING
            return
        
        enemy.set_target(None)
        # Attack player

    def alert(self, enemy, player, terrain):
        # Compute distance to player, if in tracking range change 
        # to preparing state 
        player_pos = np.array(player.get_position(), dtype=np.float64)
        enemy_pos = np.array(enemy.get_position(), dtype=np.float64)
        
        diff_vector = player_pos - enemy_pos

        distance = np.linalg.norm(diff_vector)
        if distance < self.tracking_range:
            self.state = EnemyState.PREPARING
            return
        
        enemy.set_target(None)
        # Moves a lot randomly
        
    def search_player(self, enemy_pos, player_pos, terrain, vision_range):
        diff_vector = player_pos - enemy_pos

        distance = np.linalg.norm(diff_vector)
        if distance <= vision_range and distance > 0:
            # If distance is less than vision range and
            # line of sight change state to PREPARING
            diff_vector /= 10.0
            ray_pos = enemy_pos.copy()

            for _ in range(10):
                ray_pos += diff_vector
                if not terrain.on_ground_point(ray_pos):
                    return False
            else:
                return True