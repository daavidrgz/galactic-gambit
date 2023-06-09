from enum import Enum, auto
import pygame
from constants.game_constants import (
    DESIGN_HEIGHT,
    DESIGN_WIDTH,
    INITIAL_USER_HEIGHT,
    INITIAL_USER_WIDTH,
)

from utils.singleton import Singleton


class Action(Enum):
    # SHOOT = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    PAUSE = auto()


class ControlSystem(metaclass=Singleton):

    __pressed_keys = None

    # Dict with the initial mapping of actions to keys
    def __init__(self):
        self.actions = {
            # Action.SHOOT: pygame.K_j,
            Action.LEFT: pygame.K_a,
            Action.RIGHT: pygame.K_d,
            Action.UP: pygame.K_w,
            Action.DOWN: pygame.K_s,
        }

    # Function that gets the value of an enum and returns if the key associated
    # to that action is pressed
    def is_active_action(self, action):
        return self.__pressed_keys[self.actions[action]]

    def is_key_pressed(self, key):
        return self.__pressed_keys[key]

    def refresh_pressed_keys(self):
        self.__pressed_keys = pygame.key.get_pressed()

    # Function to rebind a key to an action
    def rebind_action(self, action, key):
        self.actions[action] = key

    def get_action_key(self, action):
        return self.actions[action]

    def is_mouse_pressed(self):
        return pygame.mouse.get_pressed()[0]

    def user_pos_to_design(self, x, y):
        user_width, user_height = pygame.display.get_window_size()
        x_ratio, y_ratio = x / user_width, y / user_height
        # Scale the mouse position to the design resolution
        return round(x_ratio * DESIGN_WIDTH), round(y_ratio * DESIGN_HEIGHT)

    def get_mouse_pos(self):
        x, y = pygame.mouse.get_pos()
        return self.user_pos_to_design(x, y)
