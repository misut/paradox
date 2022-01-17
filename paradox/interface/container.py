from dependency_injector import containers, providers
from postoffice import InMemoryPostbus
from pygame import Surface
from pygame.constants import *

from paradox.application import ParadoxAtelier, ParadoxPostoffice
from paradox.domain import IntroPalette


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    postbus = providers.Singleton(InMemoryPostbus)
    postoffice = providers.Singleton(ParadoxPostoffice)

    atelier = providers.Singleton(ParadoxAtelier)
    render_screen = providers.Singleton(
        Surface,
        size=config.RENDER_SIZE,
        flags=SRCALPHA,
    )

    intro_palette = providers.Singleton(IntroPalette)
