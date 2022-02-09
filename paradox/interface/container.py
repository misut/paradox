import pygame
from dependency_injector import containers, providers
from postoffice import InMemoryPostbus
from pygame import Surface

from paradox.application import FilmDirector, UIManager, UniverseSimulator
from paradox.infrastructure import FileSpriteRepository, FileUniverseRepository


class Container(containers.DeclarativeContainer):
    base_config = providers.Configuration()
    gamepad_config = providers.Configuration()
    graphic_config = providers.Configuration()

    postbus = providers.Singleton(InMemoryPostbus)

    render_screen = providers.Singleton(
        Surface,
        size=graphic_config.RENDER_SIZE,
        flags=pygame.SRCALPHA,
    )
    sprites = providers.Singleton(
        FileSpriteRepository,
        base_config.SPRITES_PATH,
    )
    universes = providers.Singleton(
        FileUniverseRepository,
        base_config.UNIVERSES_PATH,
    )

    film_director = providers.Singleton(FilmDirector)
    ui_manager = providers.Singleton(
        UIManager,
        pos=(0, 0),
        size=graphic_config.RENDER_SIZE,
    )
    universe_simulator = providers.Singleton(
        UniverseSimulator,
        sprites=sprites.provided,
    )
