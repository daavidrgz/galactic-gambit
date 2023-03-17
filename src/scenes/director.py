import numpy as np
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
from systems.resource_manager import Resource, ResourceManager
from utils.singleton import Singleton


class Director(metaclass=Singleton):
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (INITIAL_USER_WIDTH, INITIAL_USER_HEIGHT), vsync=True
        )
        self.full_screen = False
        self.virtual_screen = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        self.crosshair = ResourceManager().load_image(Resource.CROSSHAIR)
        pygame.display.set_caption("Space Mission")
        pygame.mouse.set_visible(False)
        # Scenes stack
        self.scenes = []
        self.__leave_scene = False
        self.__do_setup = True
        self.__do_pop_back = False
        self.clock = pygame.time.Clock()

    def toggle_full_screen(self):
        self.full_screen = not self.full_screen
        pygame.display.toggle_fullscreen()

    def __loop(self, scene):
        self.__leave_scene = False
        if self.__do_setup:
            scene.setup()

        if self.__do_pop_back:
            scene.pop_back()

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
            mouse_pos = np.array(control_system.get_mouse_pos())
            cross_hair_size = np.array(self.crosshair.get_size())
            self.virtual_screen.blit(self.crosshair, mouse_pos - cross_hair_size / 2)

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
        self.__do_setup = do_setup
        self.__do_pop_back = False

    def pop_scene(self, do_pop_back=True):
        self.__leave_scene = True

        if len(self.scenes) > 0:
            self.scenes.pop()

        self.__do_pop_back = do_pop_back
        self.__do_setup = False

    def switch_scene(self, scene, do_setup=True):
        self.__leave_scene = True

        if len(self.scenes) > 0:
            self.scenes.pop()
        self.scenes.append(scene)
        self.__do_setup = do_setup
        self.__do_pop_back = False

    def leave_game(self):
        self.__leave_scene = True
        self.scenes = []

    def clear_scenes(self):
        self.scenes = []
