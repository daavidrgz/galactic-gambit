import pygame
from constants.game_constants import (
    INITIAL_USER_HEIGHT,
    INITIAL_USER_WIDTH,
    DESIGN_HEIGHT,
    DESIGN_WIDTH,
    TARGET_FRAMERATE,
    DESIGN_FRAMERATE,
)
from systems.control_system import ControlSystem
from utils.singleton import Singleton


class Director(metaclass=Singleton):
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (INITIAL_USER_WIDTH, INITIAL_USER_HEIGHT), vsync=True
        )
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
            self.user_screen_size = pygame.display.get_window_size()
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
            frame = pygame.transform.scale(self.virtual_screen, self.user_screen_size)
            self.screen.blit(frame, frame.get_rect())
            pygame.display.flip()

    def run(self):
        while len(self.scenes) > 0:
            current_scene = self.scenes[-1]
            self.__loop(current_scene)

    def push_scene(self, scene, do_setup=True):
        self.__leave_scene = True
        self.scenes.append(scene)
        if do_setup:
            scene.setup()

    def pop_scene(self):
        self.__leave_scene = True

        if len(self.scenes) > 0:
            self.scenes.pop()
            if len(self.scenes) > 0:
                self.scenes[-1].pop_back()

    def __pop_scene_without_pop_back(self):
        self.__leave_scene = True

        if len(self.scenes) > 0:
            self.scenes.pop()

    def switch_scene(self, scene, do_setup=True):
        self.__pop_scene_without_pop_back()
        self.scenes.append(scene)
        if do_setup:
            scene.setup()

    def leave_game(self):
        self.__leave_scene = True
        self.scenes = []

    def get_scene(self):
        return self.scenes[-1]

    def clear_scenes(self):
        self.scenes = []
