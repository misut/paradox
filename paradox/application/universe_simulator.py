from itertools import product

import pygame
from pydantic import BaseModel
from pygame import Surface

from paradox.domain import SpriteRepository, Universe
from paradox.domain.constants import *


class UniverseSimulator(BaseModel):
    sprites: SpriteRepository
    universe: Universe

    class Config:
        arbitrary_types_allowed = True

    def look_at(self, coo: tuple[float, float, float], zoom: float = 1.0) -> None:
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

            lwall_pixel = (
                pixel[0] - WALL_WIDTH,
                pixel[1] - (TILE_HEIGHT - WALL_HEIGHT),
            )
            lwall_sprite = self.sprites.get(tile.lwall)
            if lwall_sprite:
                render_screen.blit(
                    lwall_sprite.surface, lwall_pixel, None, special_flags
                )

            rwall_pixel = (pixel[0], pixel[1] - (TILE_HEIGHT - WALL_HEIGHT))
            rwall_sprite = self.sprites.get(tile.rwall)
            if rwall_sprite:
                render_screen.blit(
                    rwall_sprite.surface, rwall_pixel, None, special_flags
                )

            slate_pixel = (pixel[0] - WALL_WIDTH, pixel[1] - SLATE_HEIGHT)
            slate_sprite = self.sprites.get(tile.slate)
            if slate_sprite:
                render_screen.blit(
                    slate_sprite.surface, slate_pixel, None, special_flags
                )

    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        render_size = render_screen.get_size()

        background = Surface(render_size, pygame.SRCALPHA)
        background.fill((0, 100, 200, 255))
        render_screen.blit(background, (0, 0), None, special_flags)

        self.render_universe(render_screen, special_flags)

    def update(self, ticks: int) -> None:
        ...
