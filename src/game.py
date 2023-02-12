import pygame, sys
from pygame.locals import *
from entities.living.player import Player
from scenes.scene_manager import scene_manager
from scenes.one_scene import OneScene

from constants import USER_WIDTH, USER_HEIGHT, DESIGN_WIDTH, DESIGN_HEIGHT


def run():

    pygame.init()

    screen = pygame.display.set_mode((USER_WIDTH, USER_HEIGHT))
    virtual_screen = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))

    pygame.display.set_caption("Game")

    run = True
    clock = pygame.time.Clock()
    initial_scene = OneScene()
    scene_manager.push_scene(initial_scene)

    while run:
        elapsed_time = clock.tick(60)
        print(elapsed_time)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        scene_manager.handle_events(events)
        scene_manager.update_scene(elapsed_time)
        scene_manager.draw_scene(virtual_screen)

        # Transform the virtual_screen in the one that the user sees
        frame = pygame.transform.scale(virtual_screen, (USER_WIDTH, USER_HEIGHT))
        screen.blit(frame, frame.get_rect())

        # Update screen
        pygame.display.flip()
        # pygame.display.update()

    pygame.quit()
