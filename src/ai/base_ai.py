from enum import Enum, auto

class EnemyState(Enum):
    IDLE = auto()
    PREPARING = auto()
    ATTACKING = auto()
    ALERT = auto()

class BaseAI():
    def __init__(self):
        self.state = EnemyState.IDLE
        self.actions = dict()
        self.actions.setdefault(self.return_to_idle)

    def run(self, enemy, player, terrain):
        self.actions.get(self.state)(enemy, player, terrain)

    def return_to_idle(self, enemy, player, terrain):
        self.state = EnemyState.IDLE
