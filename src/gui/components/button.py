from gui.components.base_gui import BaseGui


class Button(BaseGui):
    def __init__(
        self,
        surface,
        action,
        on_select,
        on_deselect,
        position,
    ):
        self.action = action
        self.on_select = on_select
        self.on_deselect = on_deselect
        self.is_selected = False

        super().__init__(surface, position)

    def execute_action(self):
        self.action()

    def select(self):
        if self.is_selected:
            return
        self.on_select()
        self.is_selected = True

    def deselect(self):
        if not self.is_selected:
            return
        self.on_deselect()
        self.is_selected = False
