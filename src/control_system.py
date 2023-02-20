from enum import Enum, auto
import pygame

from utils.singleton import Singleton

# Enum de las acciones que hay
class Actions(Enum):
    SHOOT = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    PAUSE = auto()


class ControlSystem(metaclass=Singleton):
    # Dict with the initial mapping of actions to keys
    def __init__(self):
        self.actions = {
            Actions.SHOOT: pygame.K_j,
            Actions.LEFT: pygame.K_a,
            Actions.RIGHT: pygame.K_d,
            Actions.UP: pygame.K_w,
            Actions.DOWN: pygame.K_s,
            Actions.PAUSE: pygame.K_p,
        }

    # Function that gets the value of an enum and returns if the key associated
    # to that action is pressed
    def is_active_action(self, action):
        return pygame.key.get_pressed()[self.actions[action]]

    # Function to rebind a key to an action
    def rebind_action(self, action, key):
        self.actions[action] = key
