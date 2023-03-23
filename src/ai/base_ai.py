from enum import Enum, auto


class AIState(Enum):
    IDLE = auto()
    PREPARING = auto()
    ATTACKING = auto()
    ALERT = auto()


class BaseAI:
    def __init__(self):
        self.state = AIState.IDLE
        self.actions = dict()
        self.actions.setdefault(self.return_to_idle)

    def run(self, enemy, player, terrain, elapsed_time):
        self.actions.get(self.state)(enemy, player, terrain, elapsed_time)

    def return_to_idle(self, enemy, player, terrain, elapsed_time):
        self.state = AIState.IDLE

    def notify(self):
        self.state = AIState.PREPARING
