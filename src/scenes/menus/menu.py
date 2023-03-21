import pygame
from scenes.scene import Scene
from systems.resource_manager import Resource


class Menu(Scene):
    def __init__(self):
        super().__init__()
        self.gui_group = pygame.sprite.Group()
        self.buttons = []
        self.go_back_button = None
        self.current_button = 0
        self.buttons_len = 0
        self.background = None
        self.disable_mouse = False
        self.clicked_button = None

    def setup(self):
        self.buttons_len = len(self.buttons)
        if self.buttons_len > 0:
            self.buttons[0].select()
        super().setup()

    def get_selected_button(self):
        return self.buttons[self.current_button]

    def previous_button(self):
        if self.current_button != 0:
            self.__select_button(self.current_button - 1)

    def next_button(self):
        if self.current_button != self.buttons_len - 1:
            self.__select_button(self.current_button + 1)

    def __select_button(self, idx):
        if self.current_button == idx:
            return
        self.buttons[self.current_button].deselect()
        self.current_button = idx
        self.buttons[self.current_button].select()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                event_pos = self.control_system.user_pos_to_design(
                    event.pos[0], event.pos[1]
                )
                self.clicked_button = None
                for element in self.gui_group:
                    if element.is_inside(event_pos):
                        self.clicked_button = element
                        break
            if event.type == pygame.MOUSEBUTTONUP:
                event_pos = self.control_system.user_pos_to_design(
                    event.pos[0], event.pos[1]
                )
                for element in self.gui_group:
                    if element.is_inside(event_pos) and element == self.clicked_button:
                        element.execute_action()
                        break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.buttons[self.current_button].execute_action()
                if event.key == pygame.K_ESCAPE:
                    if self.go_back_button:
                        self.go_back_button.execute_action()

    def update(self, elapsed_time):
        if self.disable_mouse:
            return
        mouse_pos = self.control_system.get_mouse_pos()
        for idx, button in enumerate(self.buttons):
            if button.is_inside(mouse_pos):
                self.__select_button(idx)

        self.gui_group.update(elapsed_time)

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        self.gui_group.draw(screen)
