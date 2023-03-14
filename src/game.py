import pygame
from pygame.locals import *
from scenes.menus.start_menu import StartMenu
from scenes.transition import Transition

from scenes.director import Director


def run():
    pygame.init()

    initial_scene = Transition(StartMenu())
    director = Director.get_instance()
    director.push_scene(initial_scene)
    director.run()

    pygame.quit()
