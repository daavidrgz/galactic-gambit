import pygame
from pygame.locals import *
from model.game_model import GameModel
from scenes.menus.start_menu import StartMenu
from systems.rng_system import RngSystem
from scenes.levels.ship.ship_level import ShipLevel
from scenes.levels.planet.planet_level import PlanetLevel
from scenes.levels.cave.cave_level import CaveLevel

from scenes.director import Director


def run():
    pygame.init()

    # RngSystem.get_instance().seed(420)
    game_model = GameModel.get_instance()

    # Load savegame
    # game_model.load()

    initial_scene = PlanetLevel()
    director = Director.get_instance()
    director.push_scene(initial_scene)
    director.run()

    # Save model
    # game_model.save()

    pygame.quit()
