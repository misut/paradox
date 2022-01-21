import pygame
from pygame import Surface

from paradox.domain import Post, SpriteRepository, Universe
from paradox.infrastructure import InMemoryUniverse


class UniverseSimulator:
    sprites: SpriteRepository
    universe: Universe

    def __init__(self, sprites: SpriteRepository, universe: Universe) -> None:
        self.sprites = sprites
        self.universe = universe

    def look_at(self, coo:tuple[float, float, float], zoom: float = 1.0) -> None:
        self.universe.camera.look_at(coo, zoom)

    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        render_size = render_screen.get_size()

        background = Surface(render_size, pygame.SRCALPHA)
        background.fill((0, 100, 200, 255))
        render_screen.blit(background, (0, 0), None, special_flags)

        self.universe.render(render_screen, special_flags)

    def simulate(self, post: Post) -> None:
        ...

    def update(self, ticks: int) -> None:
        ...
