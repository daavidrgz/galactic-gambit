import pygame
from constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.button import Button
from gui.title import Title
from scenes.menu.menu import Menu
from scenes.test_level import TestLevel


class StartMenu(Menu):
    def __init__(self):
        super().__init__()
        background_image = self.resource_manager.load_image(
            self.resource_manager.SPACE_BACKGROUND
        )
        bg_width, bg_height = background_image.get_size()
        background_image = pygame.transform.scale(
            background_image,
            (
                (DESIGN_HEIGHT / bg_height) * bg_width,
                DESIGN_HEIGHT,
            ),
        )

        veil = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        veil.set_alpha(10)

        background = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        background.blit(background_image, (0, 0))
        background.blit(veil, (0, 0))
        self.background = background

        self.first_draw = True

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

        self.title = Title(
            text="Space Mission",
            font=self.resource_manager.load_font(self.resource_manager.FONT_XL),
            color=bright,
            position=(DESIGN_WIDTH / 2, 100),
        )

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

        self.gui_group.add(self.title, self.buttons)
