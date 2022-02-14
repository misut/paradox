from itertools import product
from math import floor

import pygame
from pydantic import BaseModel, Field
from pygame import Surface

from paradox.domain import Action, ActionInfo, Apparition, Direction, SpriteRepository, Universe
from paradox.domain.constants import *


class UniverseSimulator(BaseModel):
    sprites: SpriteRepository
    universe: Universe

    paused: bool = Field(default=False)

    class Config:
        arbitrary_types_allowed = True

    def act(self, action_infos: dict[Action, ActionInfo]) -> None:
        actor = self.universe.camera.attached if self.universe.camera.attached else self.universe.camera

        if not action_infos:
            actor.velocity = 0.0
            return

        if Action.UP in action_infos and Action.LEFT in action_infos:
            actor.direction = Direction.NORTHWEST
        elif Action.UP in action_infos and Action.RIGHT in action_infos:
            actor.direction = Direction.NORTHEAST
        elif Action.DOWN in action_infos and Action.LEFT in action_infos:
            actor.direction = Direction.SOUTHWEST
        elif Action.DOWN in action_infos and Action.RIGHT in action_infos:
            actor.direction = Direction.SOUTHEAST
        elif Action.UP in action_infos:
            actor.direction = Direction.NORTH
        elif Action.DOWN in action_infos:
            actor.direction = Direction.SOUTH
        elif Action.LEFT in action_infos:
            actor.direction = Direction.WEST
        elif Action.RIGHT in action_infos:
            actor.direction = Direction.EAST
        
        actor.velocity = 7.0

    def look_at(self, coo: tuple[float, float, float], zoom: float = 1.0) -> None:
        self.universe.camera.look_at(coo, zoom)

    def pause(self) -> None:
        self.paused = True

    def place(self, apparition: Apparition) -> None:
        self.universe.place(apparition)

    def resume(self) -> None:
        self.paused = False

    def render_background(self, render_screen: Surface, special_flags: int = 0) -> None:
        render_size = render_screen.get_size()

        background = Surface(render_size, pygame.SRCALPHA)
        background.fill((110, 190, 230, 255))
        render_screen.blit(background, (0, 0), None, special_flags)

    def render_universe(self, render_screen: Surface, special_flags: int = 0) -> None:
        apparition_blit_sequences = {}
        blit_sequences = {}
        for apparition in self.universe.apparitions:
            apparition_sprite = self.sprites.get(apparition.sprite)
            pixel = self.universe.camera.pixel(apparition.coo)
            apparition_pixel = (pixel[0] - apparition_sprite.width // 2, pixel[1] - apparition_sprite.height)

            roo = tuple(map(floor, apparition.coo))
            if roo not in apparition_blit_sequences:
                apparition_blit_sequences[roo] = []
            apparition_blit_sequences[roo].append((apparition_sprite.surface, apparition_pixel, None, special_flags))

        cur = self.universe.camera.at
        sight = self.universe.camera.sight
        for (x, y) in product(
            range(cur[0] - sight, cur[0] + sight + 1),
            range(cur[1] - sight, cur[1] + sight + 1),
        ):
            #if not (-sight <= x + y <= sight and -sight <= x - y <= sight):
                #continue
            
            tile = self.universe.at((x, y))
            pixel = self.universe.camera.pixel((x, y))

            if tile.roo not in blit_sequences:
                blit_sequences[tile.roo] = []

            if (x, y) in apparition_blit_sequences:
                blit_sequences[(x, y)].extend(apparition_blit_sequences[x, y])

            lwall_pixel = (
                pixel[0] - WALL_WIDTH,
                pixel[1] + (TILE_HEIGHT - WALL_HEIGHT),
            )
            lwall_sprite = self.sprites.get(tile.lwall)
            if lwall_sprite:
                blit_sequence = (lwall_sprite.surface, lwall_pixel, None, special_flags)
                blit_sequences[tile.roo].insert(0, blit_sequence)

            rwall_pixel = (pixel[0], pixel[1] + (TILE_HEIGHT - WALL_HEIGHT))
            rwall_sprite = self.sprites.get(tile.rwall)
            if rwall_sprite:
                blit_sequence = (rwall_sprite.surface, rwall_pixel, None, special_flags)
                blit_sequences[tile.roo].insert(0, blit_sequence)

            slate_pixel = (pixel[0] - WALL_WIDTH, pixel[1])
            slate_sprite = self.sprites.get(tile.slate)
            if slate_sprite:
                blit_sequence = (slate_sprite.surface, slate_pixel, None, special_flags)
                blit_sequences[tile.roo].insert(0, blit_sequence)

        for (x, y) in product(
            range(cur[0] - sight, cur[0] + sight + 1),
            range(cur[1] - sight, cur[1] + sight + 1),
        ):
            render_screen.blits(blit_sequences.get((x, y), []), doreturn=False)

    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        self.render_background(render_screen, special_flags)
        self.render_universe(render_screen, special_flags)

    def update(self, ticks: int) -> None:
        if self.paused:
            return

        self.sprites.update(ticks)
        if self.universe.camera.attached:
            self.universe.camera.attached.update(ticks)
        else:
            self.universe.camera.update(ticks)
