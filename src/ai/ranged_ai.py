import numpy as np

from ai.base_ai import BaseAI, EnemyState

class RangedAI(BaseAI):
    def __init__(self, vision_range, tracking_range):
        super().__init__()
        self.vision_range = vision_range
        self.tracking_range = tracking_range
        
        self.actions[EnemyState.IDLE] = self.idle
        self.actions[EnemyState.PREPARING] = self.preparing
    
    def idle(self, enemy, player, terrain):
        # Compute distance to player
        player_pos = np.array(player.get_position(), dtype=np.float64)
        enemy_pos = np.array(enemy.get_position(), dtype=np.float64)
        
        diff_vector = player_pos - enemy_pos

        distance = np.linalg.norm(diff_vector)
        if distance <= self.vision_range and distance > 0:
            # If distance is less than vision range and
            # line of sight change state to PREPARING
            diff_vector = diff_vector / distance * (self.vision_range / 10.0)
            ray_pos = enemy_pos.copy()

            for _ in range(10):
                ray_pos += diff_vector
                if terrain.on_ground_point(ray_pos):
                    break
            else:
                self.state = EnemyState.PREPARING
                return
            
        # TODO: If the distance to the player is too big or
        # there is no line of sight wander around
        
    def preparing(self, enemy, player, terrain):
        print("I am preparing!")