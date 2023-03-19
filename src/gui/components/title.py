from gui.components.base_gui import BaseGui
from gui.components.text import Text
from systems.resource_manager import Resource, ResourceManager


class Title(Text):
    def __init__(self, text, color, position):
        self.resource_manager = ResourceManager.get_instance()
        font = self.resource_manager.load_font(Resource.FONT_XL)
        font.set_bold(True)
        super().__init__(text, font, color, position)
