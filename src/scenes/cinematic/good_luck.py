from scenes.cinematic.story_scene import StoryScene
from scenes.levels.ship.ship_level import ShipLevel


class GoodLuck(StoryScene):
    def __init__(self):
        title = "Good Luck"
        argument = [
            "You are the only one who can do it.",
            "Good luck.",
        ]
        next_scene = ShipLevel
        super().__init__(title=title, argument=argument, next_scene=next_scene)
