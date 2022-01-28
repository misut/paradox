from itertools import product

import pygame
from pygame import Surface

from paradox.domain import Post, SpriteRepository, Universe


class UniverseSimulator:
    sprites: SpriteRepository
    universe: Universe

    def __init__(self, sprites: SpriteRepository, universe: Universe) -> None:
        self.sprites = sprites
        self.universe = universe

    def look_at(self, coo:tuple[float, float, float], zoom: float = 1.0) -> None:
        self.universe.camera.look_at(coo, zoom)

    def render_universe(self, render_screen: Surface, special_flags: int = 0) -> None:
        cur = self.universe.camera.at
        sight = self.universe.camera.sight
        for (x, y, z) in product(
            range(cur[0] - sight[0], cur[0] + sight[0] + 1),
            range(cur[1] - sight[1], cur[1] + sight[1] + 1),
            range(cur[2] - sight[2], cur[2] + sight[2] + 1),
        ):
            tile = self.universe.at((x, y, z))
            pixel = self.universe.camera.pixel((x, y, z))

            lwall_pixel = (pixel[0] - 29, pixel[1] - 16)
            lwall_sprite = self.sprites.get(tile.lwall)
            if lwall_sprite:
                render_screen.blit(lwall_sprite.surface, lwall_pixel, None, special_flags)

            rwall_pixel = (pixel[0], pixel[1] - 16)
            rwall_sprite = self.sprites.get(tile.rwall)
            if rwall_sprite:
                render_screen.blit(rwall_sprite.surface, rwall_pixel, None, special_flags)

            slate_pixel = (pixel[0] - 29, pixel[1] - 33)
            slate_sprite = self.sprites.get(tile.slate)
            if slate_sprite:
                render_screen.blit(slate_sprite.surface, slate_pixel, None, special_flags)
        
    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        render_size = render_screen.get_size()

        background = Surface(render_size, pygame.SRCALPHA)
        background.fill((0, 100, 200, 255))
        render_screen.blit(background, (0, 0), None, special_flags)

        self.render_universe(render_screen, special_flags)

    def simulate(self, post: Post) -> None:
        ...

    def update(self, ticks: int) -> None:
        ...
