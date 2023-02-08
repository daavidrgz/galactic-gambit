import pygame, sys
from pygame.locals import *
from entities.living.player import Player


def run():

    pygame.init()

    BLACK = (0, 0, 0)

    USER_WIDTH = 720
    USER_HEIGHT = 720

    DESIGN_WIDTH = 720
    DESIGN_HEIGHT = 720

    screen = pygame.display.set_mode((USER_WIDTH, USER_HEIGHT))
    virtual_screen = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))

    pygame.display.set_caption("Game")

    player = Player((DESIGN_WIDTH // 2, DESIGN_HEIGHT // 2))

    player_group = pygame.sprite.GroupSingle(player)

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        virtual_screen.fill(BLACK)
        player_group.draw(virtual_screen)

        # Transform the virtual_screen in the one that the user sees
        frame = pygame.transform.scale(virtual_screen, (USER_WIDTH, USER_HEIGHT))
        screen.blit(frame, frame.get_rect())

        # Update screen
        pygame.display.flip()
        # pygame.display.update()

    pygame.quit()
