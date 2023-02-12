from scenes.scene import Scene
import pygame


class AnotherScene(Scene):
    def __init__(self):
        super().__init__()
        self.name = "Another Scene"

    def draw_scene(self, screen):
        BLACK = (0, 0, 0)
        # screen.fill(BLACK)
        # Draw a green rectable in the screen
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(30, 30, 60, 60))

    def update_scene(self, elapsed_time):
        print(f"im in {self.name}")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(f"leaving {self.name}")
                    self.scene_manager.pop_scene()
