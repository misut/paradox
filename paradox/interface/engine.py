import sys

from atelier import Atelier
from loguru import logger
from postoffice import Postbus, Postoffice
from pygame import Surface
from pygame.transform import scale
import pygame

from paradox.domain import (
    Palette,
    LayoutUI,
    TextUI,
)
from paradox.interface import delivery_protocols, portraying_methods
from paradox.interface.container import Container
from paradox.interface.delivery_protocols import propagate_event_to_post
from paradox.interface.settings import Settings
import paradox


class Engine:
    container: Container
    settings: Settings

    atelier: Atelier
    postoffice: Postoffice
    screen: Surface

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        self.container = Container()
        self.container.config.from_pydantic(settings)
        self.container.wire(packages=[paradox])

        self.initialize(settings)

        self.start()

    def initialize_palette(self, settings: Settings) -> None:
        self.container.intro_palette.reset()

    def initialize_ui(self, settings: Settings) -> None:
        self.container.ui_manager.reset()
        ui_manager = self.container.ui_manager()

        intro_ui = LayoutUI(pos=(0, 0), size=settings.RENDER_SIZE)

        sample_text = TextUI(pos=(100, 100), size=(200, 50), text="Hello, world!")
        @sample_text.on_hover()
        def hover_actor() -> None:
            logger.info("wow")
        intro_ui.allocate(sample_text)

        ui_manager.allocate(intro_ui)


    def initialize(self, settings: Settings) -> None:
        pygame.init()
        pygame.display.set_caption("Hello, world!")

        logger.remove()
        logger.add(sys.stderr, level="INFO")

        self.atelier = Atelier()
        self.atelier.recruit(portraying_methods.root_portrayer)

        self.postoffice = Postoffice()
        self.postoffice.hire(delivery_protocols.chief_postman)

        self.screen = pygame.display.set_mode(
            size=settings.SCREEN_SIZE,
        )

        self.initialize_palette(settings)
        self.initialize_ui(settings)
    
    def update_posts(self, postbus: Postbus, postoffice: Postoffice) -> None:
        for event in pygame.event.get():
            post = propagate_event_to_post(
                event,
                self.settings.RENDER_SIZE,
                self.settings.SCREEN_SIZE
            )
            if post is not None:
                postoffice.request(post)

        postoffice.transport(postbus)

    def update(self) -> None:
        postbus = self.container.postbus()

        self.update_posts(postbus, self.postoffice)

    def render_portrait(self, atelier: Atelier, palette: Palette) -> None:
        atelier.portray(palette)

    def render(self) -> None:
        intro_palette = self.container.intro_palette()
        self.render_portrait(self.atelier, intro_palette)

        render_screen = self.container.render_screen()
        scaled_screen = scale(render_screen, self.settings.SCREEN_SIZE)
        self.screen.blit(scaled_screen, (0, 0))
        pygame.display.flip()

    def start(self) -> None:
        while True:
            self.update()
            self.render()
