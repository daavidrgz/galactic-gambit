import pygame
from constants import DESIGN_HEIGHT, DESIGN_WIDTH
from gui.rebind_button import RebindButton
from gui.button import Button
from gui.title import Title
from scenes.menu.menu import Menu
from systems.control_system import Actions, ControlSystem
from systems.resource_manager import Resource


class ConfigurationMenu(Menu):
    COLOR_SUBTLE = (100, 100, 100)
    COLOR_BRIGHT = (255, 255, 255)

    def __init__(self):
        super().__init__()
        veil = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        self.background = veil
        self.control_system = ControlSystem.get_instance()
        self.is_rebinding = False

    def __select_rebind_button(self):
        self.is_rebinding = True

    def __go_back(self):
        self.director.pop_scene()

    def update(self, elapsed_time):
        super().update(elapsed_time)
        if not self.is_rebinding:
            return

    def __create_action_button(self, text, action, offset):
        font = self.resource_manager.load_font(Resource.FONT_MD)

        return RebindButton(
            action_text=text,
            bind_action=action,
            bind_key=self.control_system.get_action_key(action),
            font=font,
            color=self.COLOR_SUBTLE,
            color_hover=self.COLOR_BRIGHT,
            action=self.__select_rebind_button,
            position=(DESIGN_WIDTH // 2, DESIGN_HEIGHT // 2 + offset),
        )

    def setup(self):
        self.title = Title(
            text="Configuration",
            font=self.resource_manager.load_font(Resource.FONT_XL),
            color=self.COLOR_BRIGHT,
            position=(DESIGN_WIDTH // 2, 100),
        )

        self.buttons.append(self.__create_action_button("Move Up", Actions.UP, -100))
        self.buttons.append(self.__create_action_button("Move Left", Actions.LEFT, -50))
        self.buttons.append(self.__create_action_button("Move Down", Actions.DOWN, 0))
        self.buttons.append(
            self.__create_action_button("Move Right", Actions.RIGHT, 50)
        )

        self.go_back_button = Button(
            text="Go back",
            font=self.resource_manager.load_font(Resource.FONT_MD),
            color=self.COLOR_SUBTLE,
            color_hover=self.COLOR_BRIGHT,
            action=self.__go_back,
            position=(DESIGN_WIDTH // 2, DESIGN_HEIGHT // 2 + 100),
        )
        self.buttons.append(self.go_back_button)

        self.gui_group.add(self.title, self.buttons)
        super().setup()

    def handle_events(self, events):
        if not self.is_rebinding:
            super().handle_events(events)
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    self.get_selected_button().reset_color()
                    self.is_rebinding = False
                    return

                self.get_selected_button().rebind_action(event.key)
                self.is_rebinding = False

    def draw(self, screen):
        screen.fill((0, 0, 0))
        super().draw(screen)
