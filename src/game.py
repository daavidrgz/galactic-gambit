import pygame, sys
from pygame.locals import *
from scenes.one_scene import OneScene

from scenes.director import Director


def run():

    pygame.init()

    initial_scene = OneScene()
    director = Director.get_instance()
    director.push_scene(initial_scene)
    director.run()

    pygame.quit()
