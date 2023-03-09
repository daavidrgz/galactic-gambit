import pygame
from pygame.locals import *
from model.game_model import GameModel
from scenes.menus.start_menu import StartMenu
from systems.rng_system import RngSystem
from scenes.test_level import TestLevel

from scenes.director import Director


def run():
    pygame.init()

    RngSystem.get_instance().seed(420)
    game_model = GameModel.get_instance()

    # Load savegame
    # game_model.load()

    initial_scene = StartMenu()
    director = Director.get_instance()
    director.push_scene(initial_scene)
    director.run()

    # Save model
    # game_model.save()

    pygame.quit()
