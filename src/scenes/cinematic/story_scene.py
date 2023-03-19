import pygame
from constants.game_constants import DESIGN_HEIGHT, DESIGN_WIDTH
from constants.gui_constants import COLOR_BRIGHT, COLOR_STANDARD, COLOR_SUBTLE
from gui.components.blink_text import BlinkText
from gui.components.text import Text
from gui.components.title import Title
from scenes.levels.ship.ship_level import ShipLevel
from scenes.scene import Scene
from scenes.transition import Transition
from systems.resource_manager import Resource


class StoryScene(Scene):
    def __init__(self, title, argument, next_scene):
        super().__init__()
        background_image = self.resource_manager.load_image(Resource.PLANETS_BG)
        bg_width, bg_height = background_image.get_size()
        background_image = pygame.transform.scale(
            background_image,
            (
                (DESIGN_HEIGHT / bg_height) * bg_width,
                DESIGN_HEIGHT,
            ),
        )

        veil = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        veil.set_alpha(40)

        background = pygame.Surface((DESIGN_WIDTH, DESIGN_HEIGHT))
        background.blit(background_image, (0, 0))
        background.blit(veil, (0, 0))
        self.background = background

        self.title = title
        self.argument = argument
        self.next_scene = next_scene
        self.gui_group = pygame.sprite.Group()
        self.scene_music = Resource.STORY_MUSIC

    def setup(self):
        font = self.resource_manager.load_font(Resource.FONT_MD)

        title = Title(
            text=self.title,
            color=COLOR_BRIGHT,
            position=(DESIGN_WIDTH // 2, 100),
        )

        self.gui_group.add(title)

        for idx, line in enumerate(self.argument):
            text = Text(
                text=line,
                font=font,
                color=COLOR_STANDARD,
                position=(DESIGN_WIDTH // 2, 200 + idx * 50),
            )
            self.gui_group.add(text)

        space_to_continue = BlinkText(
            text="Press space to continue",
            font=font,
            color=COLOR_SUBTLE,
            position=(0, 0),
            blink_time=1000,
        )
        space_to_continue.set_position(
            (
                DESIGN_WIDTH / 2,
                DESIGN_HEIGHT - space_to_continue.image.get_height() - 10,
            ),
        )
        self.gui_group.add(space_to_continue)

        skip_to_exit = BlinkText(
            text="ESC to skip",
            font=self.resource_manager.load_font(Resource.FONT_SM),
            color=COLOR_STANDARD,
            position=(0, 0),
            blink_time=4000,
            only_once=True,
        )
        skip_to_exit.set_position(
            (
                DESIGN_WIDTH - skip_to_exit.image.get_width() / 2 - 10,
                DESIGN_HEIGHT - skip_to_exit.image.get_height() / 2 - 10,
            ),
        )
        self.gui_group.add(skip_to_exit)

        super().setup()

    def update(self, elapsed_time):
        self.gui_group.update(elapsed_time)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.director.switch_scene(Transition(ShipLevel()))
                if event.key == pygame.K_SPACE:
                    self.director.switch_scene(Transition(self.next_scene()))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.gui_group.draw(screen)
