import itertools
import pygame
from constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.button import Button
from scenes.scene import Scene
from scenes.test_level import TestLevel


class StartMenu(Scene):
    def __init__(self):
        super().__init__()
        self.background = (0, 0, 0)
        self.gui_group = pygame.sprite.Group()
        self.buttons = []
        self.current_button = 0
        self.buttons_len = 0

    def __new_game(self):
        self.director.push_scene(TestLevel())

    def __continue_game(self):
        current_level = self.game_model.get_level()
        self.director.push_scene(current_level)

    def __leave_game(self):
        self.director.leave_game()

    def __config_game(self):
        pass

    def setup(self):
        subtle = (100, 100, 100)
        bright = (255, 255, 255)
        font = self.resource_manager.load_font(self.resource_manager.FONT_LG)

        self.continue_game_button = Button(
            text="Continue Game",
            font=font,
            color=subtle,
            color_hover=bright,
            action=self.__continue_game,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2),
        )

        self.new_game_button = Button(
            text="New Game",
            font=font,
            color=subtle,
            color_hover=bright,
            action=self.__new_game,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2),
        )

        self.config_game_button = Button(
            text="Configuration",
            font=font,
            color=subtle,
            color_hover=bright,
            action=self.__config_game,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2),
        )

        self.quit_game_button = Button(
            text="Quit Game",
            font=font,
            color=subtle,
            color_hover=bright,
            action=self.__leave_game,
            position=(DESIGN_WIDTH / 2, DESIGN_HEIGHT / 2),
        )

        if self.game_model.save_exists():
            self.continue_game_button.set_position_rel((0, -150))
            self.new_game_button.set_position_rel((0, -50))
            self.config_game_button.set_position_rel((0, 50))
            self.quit_game_button.set_position_rel((0, 150))
            self.buttons.append(self.continue_game_button)
        else:
            self.new_game_button.set_position_rel((0, -100))
            self.quit_game_button.set_position_rel((0, 100))

        self.buttons.append(self.new_game_button)
        self.buttons.append(self.config_game_button)
        self.buttons.append(self.quit_game_button)

        self.buttons_len = len(self.buttons)
        self.buttons[0].select()

        self.gui_group.add(self.buttons)

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
                    self.buttons[self.current_button].action()

    def update(self, elapsed_time):
        self.gui_group.update(elapsed_time)

    def draw(self, screen):
        screen.fill(self.background)
        self.gui_group.draw(screen)
