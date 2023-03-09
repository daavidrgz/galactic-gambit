import pygame
from scenes.scene import Scene


class Menu(Scene):
    def __init__(self):
        super().__init__()
        self.gui_group = pygame.sprite.Group()
        self.buttons = []
        self.current_button = 0
        self.buttons_len = 0
        self.background = None
        self.is_first_draw = True

    def get_selected_button(self):
        return self.buttons[self.current_button]

    def setup(self):
        self.buttons_len = len(self.buttons)
        if self.buttons_len > 0:
            self.buttons[0].select()

    def handle_events(self, events):
        for event in events:
            # Uncomment if you want mouse interaction
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     self.clicked_element = None
            #     for element in self.gui_group:
            #         if element.is_inside(event.pos):
            #             self.clicked_element = element
            #             break
            # if event.type == pygame.MOUSEBUTTONUP:
            #     for element in self.gui_group:
            #         if element.is_inside(event.pos) and element == self.clicked_element:
            #             element.action()
            #             break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.current_button != 0:
                        self.buttons[self.current_button].deselect()
                        self.current_button -= 1
                        self.buttons[self.current_button].select()
                if event.key == pygame.K_DOWN:
                    if self.current_button != self.buttons_len - 1:
                        self.buttons[self.current_button].deselect()
                        self.current_button += 1
                        self.buttons[self.current_button].select()
                if event.key == pygame.K_RETURN:
                    self.buttons[self.current_button].execute_action()

    def update(self, elapsed_time):
        self.gui_group.update(elapsed_time)

    def draw(self, screen):
        if self.background is not None:
            screen.blit(self.background, (0, 0))
        self.gui_group.draw(screen)
