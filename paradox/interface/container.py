import pygame
from dependency_injector import containers, providers
from postoffice import InMemoryPostbus
from pygame import Surface

from paradox.application import Gamepad, UIManager, UniverseSimulator
from paradox.infrastructure import FileSpriteRepository, FileUniverseRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    postbus = providers.Singleton(InMemoryPostbus)

    render_screen = providers.Singleton(
        Surface,
        size=config.RENDER_SIZE,
        flags=pygame.SRCALPHA,
    )
    sprites = providers.Singleton(
        FileSpriteRepository,
        config.SPRITES_PATH,
    )
    universes = providers.Singleton(
        FileUniverseRepository,
        config.UNIVERSES_PATH,
    )

    gamepad = providers.Singleton(
        Gamepad,
    )
    ui_manager = providers.Singleton(
        UIManager,
        pos=(0, 0),
        size=config.RENDER_SIZE,
    )
    universe_simulator = providers.Singleton(
        UniverseSimulator,
        sprites=sprites.provided,
    )
