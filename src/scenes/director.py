import pygame
from constants import (
    USER_HEIGHT,
    USER_WIDTH,
    DESIGN_HEIGHT,
    DESIGN_WIDTH,
    TARGET_FRAMERATE,
    DESIGN_FRAMERATE,
)
from systems.control_system import ControlSystem
from systems.camera_manager import CameraManager
from utils.singleton import Singleton


class Director(metaclass=Singleton):
    def __init__(self):
        self.screen = pygame.display.set_mode((USER_WIDTH, USER_HEIGHT))
        self.virtual_screen = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        pygame.display.set_caption("Game")
        # Scenes stack
        self.scenes = []
        self.__leave_scene = False
        self.clock = pygame.time.Clock()

    def __loop(self, scene):
        self.__leave_scene = False
        pygame.event.clear()

        control_system = ControlSystem.get_instance()

        while not self.__leave_scene:
            elapsed_time = self.clock.tick(TARGET_FRAMERATE)

            # Intentional slowdown when under half the design framerate
            elapsed_time = min(2000 / DESIGN_FRAMERATE, elapsed_time)

            events = pygame.event.get()

            control_system.refresh_pressed_keys()

            for event in events:
                if event.type == pygame.QUIT:
                    self.leave_game()
                    return

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
        scene.setup()

    def pop_scene(self):
        self.__leave_scene = True

        if len(self.scenes) > 0:
            self.scenes.pop()
            if len(self.scenes) > 0:
                self.scenes[-1].pop_back()

    def switch_scene(self, scene):
        self.pop_scene()
        self.scenes.append(scene)
        scene.setup()

    def leave_game(self):
        self.__leave_scene = True
        self.scenes = []

    def get_scene(self):
        return self.scenes[-1]

    def clear_scenes(self):
        self.scenes = []
