from scenes.cinematic.story_scene import StoryScene
from scenes.levels.ship.ship_level import ShipLevel


class StoryIntro(StoryScene):
    def __init__(self):
        title = "The Beginning"
        argument = [
            "The earth is dying. The sun is dying. The universe is dying.",
            "The only way to save it is to go back in time and stop the cause of the problem.",
            "You are the only one who can do it.",
        ]
        next_scene = ShipLevel
        super().__init__(title=title, argument=argument, next_scene=next_scene)
