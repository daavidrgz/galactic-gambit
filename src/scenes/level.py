from scenes.scene import Scene
from systems.camera_manager import ScrollableGroup

class Level(Scene):
    def __init__(self, generator, terrain, player, background_color):
        self.generator = generator
        self.terrain = terrain
        self.player = player
        self.background_color = background_color

        self.player_group = ScrollableGroup(player)
        
        super().__init__()

    def setup(self):
        self.player.setup()
        self.generator.generate()

    def update(self, elapsed_time):
        self.player.update(elapsed_time)

    def handle_events(self, events):
        pass

    def draw(self, screen):
        screen.fill(self.background_color)
        self.terrain.draw(screen)
        self.player_group.draw(screen)

    def pop_back(self):
        pass