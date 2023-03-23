from scenes.cinematic.story_scene import StoryScene
from scenes.cinematic.the_signal_story import TheSignalStory


class TheBeginningStory(StoryScene):
    def __init__(self):
        title = "The Beginning"
        argument = [
            "Year 2084. The quick technological progress",
            "that boosted us through the start of the century",
            "has now been replaced by conflicts and misery.",
            "",
            "Taking advantage of the few brief periods of stability,",
            "the Lancestar Federation has been preparing",
            "to precipitate the next great breakthrough...",
        ]
        next_scene = TheSignalStory
        super().__init__(title=title, argument=argument, next_scene=next_scene)
