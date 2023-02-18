import pygame
from constants import USER_HEIGHT, USER_WIDTH, DESIGN_HEIGHT, DESIGN_WIDTH, TARGET_FRAMERATE


class Director:
    __instance = None

    def __init__(self):
        self.screen = pygame.display.set_mode((USER_WIDTH, USER_HEIGHT))
        self.virtual_screen = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        pygame.display.set_caption("Game")
        # Scenes stack
        self.scenes = []
        self.__leave_scene = False
        self.clock = pygame.time.Clock()

    def get_instance():
        if Director.__instance is None:
            Director.__instance = Director()
        return Director.__instance

    def __loop(self, scene):
        self.__leave_scene = False
        pygame.event.clear()

        while not self.__leave_scene:
            elapsed_time = self.clock.tick(TARGET_FRAMERATE)

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.leave_game()
            # Handle events in scene
            scene.handle_events(events)

            # Update scene
            scene.update(elapsed_time)

            # Draw scene
            scene.draw(self.virtual_screen)
            # Re-scale the virtual screen to the user screen
            frame = pygame.transform.scale(
                self.virtual_screen, (USER_WIDTH, USER_HEIGHT)
            )
            self.screen.blit(frame, frame.get_rect())
            pygame.display.flip()

    def run(self):
        while len(self.scenes) > 0:
            current_scene = self.scenes[-1]
            self.__loop(current_scene)

    def push_scene(self, scene):
        self.__leave_scene = True
        self.scenes.append(scene)

    def pop_scene(self):
        self.__leave_scene = True

        if len(self.scenes) > 0:
            self.scenes.pop()

    def switch_scene(self, scene):
        self.pop_scene()
        self.scenes.append(scene)

    def leave_game(self):
        self.__leave_scene = True
        self.scenes = []
