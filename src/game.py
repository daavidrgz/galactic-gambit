import pygame, sys
from pygame.locals import *
from entities.living.player.player import Player
from model.game_model import GameModel
from rng_system import Generator, RngSystem
from scenes.one_scene import OneScene

from scenes.director import Director


def run():

    pygame.init()

    RngSystem.get_instance().seed(420)
    game_model = GameModel.get_instance()

    # Load savegame
    # game_model.load()

    initial_scene = OneScene()
    director = Director.get_instance()
    director.push_scene(initial_scene)
    director.run()

    # Save model
    # game_model.save()

    pygame.quit()
