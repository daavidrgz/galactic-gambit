from constants import DESIGN_WIDTH, DESIGN_HEIGHT


class Scroll:
    __scroll_width = DESIGN_WIDTH
    __scroll_height = DESIGN_HEIGHT

    def __init__(self, initial_scroll):
        self.scrollx, self.scrolly = initial_scroll

    def get_scroll(self):
        return self.scrollx, self.scrolly

    def set_scroll(self, scroll):
        self.scrollx, self.scrolly = scroll

    def move_scroll(self, scroll):
        deltax, deltay = scroll
        self.scrollx += deltax
        self.scrolly += deltay

    def center_at(self, sprite):
        self.scrollx = sprite.x - DESIGN_WIDTH // 2
        self.scrolly = sprite.y - DESIGN_HEIGHT // 2
        return self
