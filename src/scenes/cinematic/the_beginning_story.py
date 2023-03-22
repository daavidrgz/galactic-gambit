from scenes.cinematic.story_scene import StoryScene
from scenes.cinematic.the_mission_story import TheMissionStory


class TheBeginningStory(StoryScene):
    def __init__(self):
        title = "Mission Briefing"
        argument = [
            "The year is 2084. The quick technological progress",
            "that boosted us through the start of the century",
            "has now been replaced by conflicts and misery.",
            "",
            "Taking advantage of the few brief periods of stability",
            "at hand, the Lancestar Federation has been",
            "preparing to precipitate the next great breakthrough.",
        ]
        next_scene = TheMissionStory
        super().__init__(title=title, argument=argument, next_scene=next_scene)
