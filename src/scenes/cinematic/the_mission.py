from scenes.cinematic.good_luck import GoodLuck
from scenes.cinematic.story_scene import StoryScene
from scenes.levels.ship.ship_level import ShipLevel


class TheMission(StoryScene):
    def __init__(self):
        title = "The Mission"
        argument = [
            "Your mission is to find the emitters in the planet's core and destroy them.",
            "The planet is full of strange creatures, so be careful.",
        ]
        next_scene = GoodLuck
        super().__init__(title=title, argument=argument, next_scene=next_scene)
