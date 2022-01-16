from dependency_injector.wiring import Provide
from postoffice import Postbus
from pygame import Surface
from pygame.transform import scale
import pygame

from paradox.applications import ParadoxAtelier, ParadoxPostoffice
from paradox.container import Container
from paradox.domain import IntroPalette, propagate_event_to_post
from paradox.settings import Settings
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

    def initialize(self, settings: Settings) -> None:
        pygame.display.set_caption("Hello, world!")
        self.screen = pygame.display.set_mode(
            size=settings.SCREEN_SIZE,
        )
    
    def update_posts(self, postbus: Postbus, postoffice: ParadoxPostoffice) -> None:
        for event in pygame.event.get():
            post = propagate_event_to_post(event)
            if post is None:
                continue

            postoffice.request(post)

        postoffice.transport(postbus)

    def update(
        self,
        postbus: Postbus = Provide[Container.postbus],
        postoffice: ParadoxPostoffice = Provide[Container.postoffice]
    ) -> None:
        self.update_posts(postbus, postoffice)

    def render_portrait(self, atelier: ParadoxAtelier, render_screen: Surface) -> None:
        atelier.portray(IntroPalette(), render_screen)

    def render(
        self,
        atelier: ParadoxAtelier = Provide[Container.atelier],
        render_screen: Surface = Provide[Container.render_screen],
    ) -> None:
        self.render_portrait(atelier, render_screen)

        scaled_screen = scale(render_screen, self.settings.SCREEN_SIZE)
        self.screen.blit(scaled_screen, (0, 0))
        pygame.display.flip()

    def start(self) -> None:
        while True:
            self.update()
            self.render()
