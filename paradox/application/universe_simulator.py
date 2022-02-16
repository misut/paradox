from itertools import product
from math import floor
from tkinter import LEFT

import pygame
from pydantic import BaseModel, Field
from pygame import Surface

from paradox.domain import (
    Action,
    ActionInfo,
    ActionType,
    Apparition,
    Direction,
    Placeable,
    SpriteRepository,
    Universe,
)
from paradox.domain.constants import *


class UniverseSimulator(BaseModel):
    sprites: SpriteRepository
    universe: Universe

    paused: bool = Field(default=False)

    class Config:
        arbitrary_types_allowed = True

    def act(self, action_infos: dict[Action, ActionInfo]) -> None:
        actor: Placeable = (
            self.universe.camera.attached
            if self.universe.camera.attached
            else self.universe.camera
        )

        actor_acceleration = 0.0
        actor_velocity = 0.0
        actor_direction = Direction.NONE
        for action, action_info in action_infos.items():
            if action_info.type == ActionType.RELEASED:
                continue

            match action:
                case Action.UP:
                    actor_direction += Direction.NORTH
                case Action.DOWN:
                    actor_direction += Direction.SOUTH
                case Action.LEFT:
                    actor_direction += Direction.WEST
                case Action.RIGHT:
                    actor_direction += Direction.EAST
            
            actor_acceleration = 30.0
            actor_velocity = actor.velocity
            
        actor.acceleration = actor_acceleration
        actor.velocity = actor_velocity
        actor.direction = actor_direction

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
        apparition_blit_sequences = [[] for _ in range(100)]
        for apparition in self.universe.apparitions:
            apparition_sprite = self.sprites.get(apparition.sprite)
            pixel = self.universe.camera.pixel(apparition.coo)
            apparition_pixel = (
                pixel[0] - apparition_sprite.width // 2,
                pixel[1] - apparition_sprite.height,
            )

            coo = tuple(map(floor, apparition.coo))
            roo = tuple(map(floor, apparition.coo))
            zidx = roo[0] - coo[0]
            apparition_blit_sequences[zidx].append(
                (apparition_sprite.surface, apparition_pixel, None, special_flags)
            )

        cur = self.universe.camera.at
        sight = self.universe.camera.sight

        stt = (cur[0] - sight, cur[1] - sight)
        pxl = self.universe.camera.pixel(stt)
        blit_sequences = [[] for _ in range(100)]
        for (x, y) in product(
            range(cur[0] - sight, cur[0] + sight),
            range(cur[1] - sight, cur[1] + sight),
        ):
            if not (-sight <= x + y - cur[0] - cur[1] <= sight and -sight <= x - y - cur[0] + cur[1] <= sight):
                continue

            tile = self.universe.at((x, y))
            diff = (x - stt[0], y - stt[1])
            pixel = (pxl[0] + (diff[0] - diff[1]) * (TILE_WIDTH // 2), pxl[1] + (diff[0] + diff[1]) * (SLATE_HEIGHT // 2))
            zidx = tile.roo[0] - tile.coo[0]

            lwall_pixel = (
                pixel[0] - (TILE_WIDTH // 2),
                pixel[1] + (SLATE_HEIGHT // 2),
            )
            lwall_sprite = self.sprites.get(tile.lwall)
            if lwall_sprite:
                blit_sequence = (lwall_sprite.surface, lwall_pixel, None, special_flags)
                blit_sequences[zidx].append(blit_sequence)

            rwall_pixel = (pixel[0], pixel[1] + (SLATE_HEIGHT // 2))
            rwall_sprite = self.sprites.get(tile.rwall)
            if rwall_sprite:
                blit_sequence = (rwall_sprite.surface, rwall_pixel, None, special_flags)
                blit_sequences[zidx].append(blit_sequence)

            slate_pixel = (pixel[0] - (TILE_WIDTH // 2), pixel[1])
            slate_sprite = self.sprites.get(tile.slate)
            if slate_sprite:
                blit_sequence = (slate_sprite.surface, slate_pixel, None, special_flags)
                blit_sequences[zidx].append(blit_sequence)

        for zidx in range(-50, 50):
            render_screen.blits(blit_sequences[zidx], doreturn=False)
            render_screen.blits(apparition_blit_sequences[zidx], doreturn=False)

    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        self.render_background(render_screen, special_flags)
        self.render_universe(render_screen, special_flags)

    def update(self, ticks: int) -> None:
        if self.paused:
            return

        self.sprites.update(ticks)
        if self.universe.camera.attached:
            self.universe.camera.attached.update(ticks)
        
        self.universe.camera.update(ticks)
