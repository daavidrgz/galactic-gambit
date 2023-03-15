import pygame
from pygame.locals import *
from scenes.levels.cave.cave_level import CaveLevel
from scenes.levels.planet.planet_level import PlanetLevel
from scenes.levels.ship.ship_level import ShipLevel
from scenes.menus.start_menu import StartMenu
from scenes.transition import Transition

from scenes.director import Director


def run():
    pygame.init()

    initial_scene = Transition(PlanetLevel())
    director = Director.get_instance()
    director.push_scene(initial_scene)
    director.run()

    pygame.quit()
