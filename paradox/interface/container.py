import pygame
from dependency_injector import containers, providers
from postoffice import InMemoryPostbus
from pygame import Surface

from paradox.application import UIManager, UniverseSimulator
from paradox.domain import IntroPalette
from paradox.infrastructure import FileSpriteRepository, FileUniverseRepository, InMemoryUniverse


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

    ui_manager = providers.Singleton(
        UIManager,
        pos=(0, 0),
        size=config.RENDER_SIZE,
    )
    # TODO: Should be removed
    universe = providers.Singleton(
        InMemoryUniverse,
        size=config.RENDER_SIZE,
    )
    universe_simulator = providers.Singleton(
        UniverseSimulator,
        sprites=sprites.provided,
        universe=universe.provided,
    )

    intro_palette = providers.Singleton(IntroPalette)
