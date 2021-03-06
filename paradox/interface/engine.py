import sys

import pygame
from loguru import logger
from postoffice import Postbus, Postoffice
from pygame import Surface
from pygame.time import Clock
from pygame.transform import scale

import paradox
from paradox.application import paradox_director
from paradox.domain import SceneNo, TickPost, universe_assets
from paradox.interface import protocols
from paradox.interface.container import Container
from paradox.interface.gamepad import Gamepad
from paradox.interface.settings import BaseSettings, GamepadSettings, GraphicSettings


class Engine:
    container: Container
    base_settings: BaseSettings
    gamepad_settings: GamepadSettings
    graphic_settings: GraphicSettings

    gamepad: Gamepad
    postoffice: Postoffice

    clock: Clock
    screen: Surface

    def __init__(
        self,
        base_settings: BaseSettings,
        gamepad_settings: GamepadSettings,
        graphic_settings: GraphicSettings,
    ) -> None:
        self.base_settings = base_settings
        self.gamepad_settings = gamepad_settings
        self.graphic_settings = graphic_settings

        self.container = Container()
        self.container.base_config.from_pydantic(base_settings)
        self.container.gamepad_config.from_pydantic(gamepad_settings)
        self.container.graphic_config.from_pydantic(graphic_settings)
        self.container.wire(packages=[paradox])
        self.container.initialize()

        self.initialize()

        self.start()

    def initialize_film_director(self) -> None:
        film_director = self.container.film_director()
        ui_manager = self.container.ui_manager()
        universe_simulator = self.container.universe_simulator()

        film_director.invite(paradox_director)
        film_director.shoot(SceneNo.INTRO, ui_manager, universe_simulator)

    def initialize_ui(self) -> None:
        pass

    def initialize_universe(self) -> None:
        self.container.universe_simulator.reset()

        universe_simulator = self.container.universe_simulator(
            universe=universe_assets.get("Paradox")
        )

    def initialize(self) -> None:
        pygame.init()
        pygame.display.set_caption("Hello, world!")

        logger.remove()
        logger.add(sys.stderr, level="INFO")

        self.gamepad = Gamepad(self.gamepad_settings, self.graphic_settings)

        self.postoffice = Postoffice()
        self.postoffice.hire(protocols.chief_postman)

        self.clock = Clock()
        self.screen = pygame.display.set_mode(
            size=self.graphic_settings.SCREEN_SIZE,
            # flags=pygame.FULLSCREEN,
        )

        self.initialize_ui()
        self.initialize_universe()
        self.initialize_film_director()

    def render(self) -> None:
        render_screen = self.container.render_screen()
        scaled_screen = scale(render_screen, self.graphic_settings.SCREEN_SIZE)
        self.screen.blit(scaled_screen, (0, 0))
        pygame.display.flip()

    def update_posts(self, postbus: Postbus) -> None:
        tick_post = TickPost(
            actions=self.gamepad.poll(self.clock.get_time()),
            fps=self.clock.get_fps(),
            ticks=self.clock.get_time(),
        )
        self.postoffice.request(tick_post)

        for post in self.gamepad.propagate():
            self.postoffice.request(post)

        self.postoffice.transport(postbus)

    def update(self) -> None:
        postbus = self.container.postbus()

        self.update_posts(postbus)

    def start(self) -> None:
        while True:
            self.render()
            self.update()
            self.clock.tick()
