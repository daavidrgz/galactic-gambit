from scenes.cinematic.good_luck_story import GoodLuckStory
from scenes.cinematic.story_scene import StoryScene


class TheMissionStory(StoryScene):
    def __init__(self):
        title = "Mission Briefing"
        argument = [
            "One fateful day, the researchers at",
            "Lancestar Space Innovations were startled",
            "by abnormal readings from their equipment.",
            "",
            "This signal... it was unlike anything they",
            "had dealt with in the past.",
            "They decided to send out a crew to investigate.",
            "However, only one person voluteered."
        ]
        next_scene = GoodLuckStory
        super().__init__(title=title, argument=argument, next_scene=next_scene)
