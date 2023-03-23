from scenes.cinematic.your_fate_story import YourFateStory
from scenes.cinematic.story_scene import StoryScene


class TheSignalStory(StoryScene):
    def __init__(self):
        title = "The Signal"
        argument = [
            "One fateful day, the researchers at",
            "Lancestar Space Innovations were startled",
            "by abnormal readings from their equipment.",
            "",
            "This signal... it was unlike anything they",
            "had dealt with in the past.",
            "They decided to send out a crew to investigate.",
            "However, only one person voluteered...",
        ]
        next_scene = YourFateStory
        super().__init__(title=title, argument=argument, next_scene=next_scene)
