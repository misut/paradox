import pygame
from dependency_injector import containers, providers
from postoffice import InMemoryPostbus
from pygame import Surface

from paradox.application import UIManager
from paradox.domain import IntroPalette


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    postbus = providers.Singleton(InMemoryPostbus)

    render_screen = providers.Singleton(
        Surface,
        size=config.RENDER_SIZE,
        flags=pygame.SRCALPHA,
    )

    ui_manager = providers.Singleton(
        UIManager,
        size=config.RENDER_SIZE,
    )

    intro_palette = providers.Singleton(IntroPalette)
