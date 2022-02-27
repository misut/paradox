from pathlib import Path

import pygame
from dependency_injector import containers, providers
from postoffice import InMemoryPostbus
from pygame import Surface

from paradox.application import FilmDirector, UIManager, UniverseSimulator
from paradox.domain import sprite_assets, universe_assets


def initialize_resources(sprites_path: Path, universes_path: Path) -> None:
    sprite_assets.initialize(sprites_path)
    universe_assets.initialize(universes_path)


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

    film_director = providers.Singleton(FilmDirector)
    ui_manager = providers.Singleton(
        UIManager,
        pos=(0, 0),
        size=graphic_config.RENDER_SIZE,
    )
    universe_simulator = providers.Singleton(
        UniverseSimulator,
    )

    initialize = providers.Resource(
        initialize_resources,
        sprites_path=base_config.SPRITES_PATH,
        universes_path=base_config.UNIVERSES_PATH,
    )
