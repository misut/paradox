from atelier import Palette
from postoffice import Postbus
from pygame import Surface
from pygame.transform import scale
import pygame

from paradox.application import ParadoxAtelier, ParadoxPostoffice
from paradox.domain import (
    IntroPalette,
    propagate_event_to_post,
    LayoutUI,
    TextUI,
)
from paradox.interface.container import Container
from paradox.interface.settings import Settings
import paradox


class Engine:
    container: Container
    screen: Surface
    settings: Settings

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        self.container = Container()
        self.container.config.from_pydantic(settings)
        self.container.wire(packages=[paradox])

        self.initialize(settings)

        self.start()

    def initialize_palette(
        self,
        settings: Settings,
    ) -> None:
        self.container.intro_palette.reset()

        intro_ui = LayoutUI(pos=(0, 0), size=settings.RENDER_SIZE)

        sample_text = TextUI(pos=(100, 100), size=(200, 50), text="Hello, world!")
        intro_ui.allocate(sample_text)

        self.container.intro_palette(ui=intro_ui)

    def initialize(self, settings: Settings) -> None:
        pygame.init()
        pygame.display.set_caption("Hello, world!")
        self.screen = pygame.display.set_mode(
            size=settings.SCREEN_SIZE,
        )

        self.initialize_palette(settings)

    def update_palettes(self, intro_palatte: IntroPalette) -> None:
        intro_palatte.ui.update()
    
    def update_posts(self, postbus: Postbus, postoffice: ParadoxPostoffice) -> None:
        for event in pygame.event.get():
            post = propagate_event_to_post(event)
            if post is not None:
                postoffice.request(post)

        postoffice.transport(postbus)

    def update(self) -> None:
        intro_palette = self.container.intro_palette()
        postbus = self.container.postbus()
        postoffice = self.container.postoffice()

        self.update_palettes(intro_palette)
        self.update_posts(postbus, postoffice)

    def render_portrait(self, atelier: ParadoxAtelier, palette: Palette, render_screen: Surface) -> None:
        atelier.portray(palette, render_screen, pygame.BLEND_ALPHA_SDL2)

    def render(self) -> None:
        atelier = self.container.atelier()
        render_screen = self.container.render_screen()

        intro_palette = self.container.intro_palette()

        self.render_portrait(atelier, intro_palette, render_screen)

        scaled_screen = scale(render_screen, self.settings.SCREEN_SIZE)
        self.screen.blit(scaled_screen, (0, 0))
        pygame.display.flip()

    def start(self) -> None:
        while True:
            self.update()
            self.render()
