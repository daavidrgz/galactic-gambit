import pygame
from gui.base_gui import BaseGui


class Button(BaseGui):
    def __init__(
        self,
        text,
        font,
        color,
        color_hover,
        action,
        position,
        background=None,
        background_hover=None,
    ):
        self.text = text
        self.action = action
        self.font = font
        self.color = color
        self.color_hover = color_hover
        self.background = background
        self.background_hover = background_hover
        self.is_selected = False

        self.current_background = background
        self.current_color = color

        self.text_surface = self.__render_font(text, color, background)

        super().__init__(self.text_surface, position)

    def execute_action(self):
        self.action()

    def __render_font(self, text, color, background):
        return self.font.render(text, True, color, background)

    def set_text(self, text):
        self.text = text
        self.image = self.__render_font(
            text, self.current_color, self.current_background
        )

    def set_color(self, color):
        self.current_color = color
        self.image = self.__render_font(self.text, color, self.background)

    def set_background(self, background):
        self.current_background = background
        self.image = self.__render_font(self.text, self.current_color, background)

    def set_position(self, position):
        self.rect.center = position

    def set_position_rel(self, position):
        deltax, deltay = position
        self.rect.center = (self.rect.center[0] + deltax, self.rect.center[1] + deltay)

    def update(self, elapsed_time):
        pass
        # if self.is_inside(pygame.mouse.get_pos()):
        #     self.select()
        # else:
        #     self.deselect()

    def select(self):
        if self.is_selected:
            return
        self.set_color(self.color_hover)
        self.is_selected = True

    def deselect(self):
        if not self.is_selected:
            return
        self.set_color(self.color)
        self.is_selected = False
