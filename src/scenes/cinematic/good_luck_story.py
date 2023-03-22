from scenes.cinematic.story_scene import StoryScene
from scenes.levels.ship.ship_level import ShipLevel


class GoodLuckStory(StoryScene):
    def __init__(self):
        title = "Mission Briefing"
        argument = [
            "He was not sufficiently trained.",
            "He was not courageous, nor strong.",
            "He was, unfortunately, our only chance.",
            "",
            "Elcien T. Ifico, your mission is to find the origin of the extraneous signal.",
            "But first, what's that noise coming from the spacecraft exterior?",
            "...",
            "May the odds be in your favor.",
        ]
        next_scene = ShipLevel
        super().__init__(title=title, argument=argument, next_scene=next_scene)
