import pygame, sys
from pygame.locals import *
from entities.living.player.player import Player
from model.game_model import GameModel
from systems.rng_system import Generator, RngSystem
from scenes.generation_test_scene import GenerationScene

from scenes.director import Director


def run():
    pygame.init()

    RngSystem.get_instance().seed(420)
    game_model = GameModel.get_instance()

    # Load savegame
    # game_model.load()

    initial_scene = GenerationScene()
    director = Director.get_instance()
    director.push_scene(initial_scene)
    director.run()

    # Save model
    # game_model.save()

    pygame.quit()
