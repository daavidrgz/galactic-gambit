import pygame
from scenes.menus.menu import Menu


class HorizontalMenu(Menu):
    def __init__(self):
        super().__init__()

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.__previous_button()
                if event.key == pygame.K_RIGHT:
                    self.__next_button()
