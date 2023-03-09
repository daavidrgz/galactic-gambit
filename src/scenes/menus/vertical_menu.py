import pygame
from scenes.menus.menu import Menu


class VerticalMenu(Menu):
    def __init__(self):
        super().__init__()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.previous_button()
                if event.key == pygame.K_DOWN:
                    self.next_button()
        super().handle_events(events)
