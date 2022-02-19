from itertools import product
from math import floor
from tkinter import LEFT
from loguru import logger

import pygame
from pydantic import BaseModel, Field
from pygame import Surface

from paradox.domain import (
    Action,
    ActionInfo,
    ActionType,
    Apparition,
    Camera,
    Direction,
    SpriteRepository,
    Universe,
)
from paradox.domain.constants import *
from paradox.domain.constants import RENDER_OFFSET


class UniverseSimulator(BaseModel):
    sprites: SpriteRepository
    universe: Universe

    paused: bool = Field(default=False)

    class Config:
        arbitrary_types_allowed = True

    def act(self, action_infos: dict[Action, ActionInfo]) -> None:
        actor: Apparition | Camera = (
            self.universe.camera.attached
            if self.universe.camera.attached
            else self.universe.camera
        )

        actor_acceleration = 0.0
        actor_direction = Direction.NONE
        actor_velocity = 0.0
        actor_gravity = 98.0
        
        for action, action_info in action_infos.items():
            if action_info.type == ActionType.RELEASED:
                continue

            if action_info.type == ActionType.PRESSED:
                if isinstance(actor, Apparition) and action == Action.JUMP:
                    if actor.jump_count < actor.jump_count_limit:
                        actor.jump()

            match action:
                case Action.UP:
                    actor_direction += Direction.NORTH
                case Action.DOWN:
                    actor_direction += Direction.SOUTH
                case Action.LEFT:
                    actor_direction += Direction.WEST
                case Action.RIGHT:
                    actor_direction += Direction.EAST
                case _:
                    continue
            
            actor_acceleration = actor.move_power
            actor_velocity = actor.velocity
            
        actor.acceleration = actor_acceleration
        if actor_direction != Direction.NONE:
            actor.direction = actor_direction
        actor.velocity = actor_velocity
        if isinstance(actor, Apparition):
            actor.gravity = actor_gravity

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
        sorted_apparitions: dict[tuple[int, int], list[Apparition]] = {}
        for apparition in self.universe.apparitions:
            coo = tuple(map(floor, apparition.coo))
            if coo not in sorted_apparitions:
                sorted_apparitions[coo] = []
            sorted_apparitions[coo].append(apparition)

        cur = self.universe.camera.at
        sight = self.universe.camera.sight

        stt = (cur[0] - sight, cur[1] - sight)
        pxl = self.universe.camera.pixel(stt)
        blit_sequences = {}

        coords = [
            (x, y) for (x, y) in product(
                range(cur[0] - sight - RENDER_OFFSET, cur[0] + sight - RENDER_OFFSET),
                range(cur[1] - sight - RENDER_OFFSET, cur[1] + sight - RENDER_OFFSET),
            ) if -sight <= x + y - cur[0] - cur[1] <= sight and -sight <= x - y - cur[0] + cur[1] <= sight
        ]
        coords.sort(key=lambda coo: coo[0] + coo[1])

        for (x, y) in coords:
            if (x, y) in sorted_apparitions:
                for apparition in sorted_apparitions[(x, y)]:
                    apparition_sprite = self.sprites.get(apparition.sprite)
                    pixel = self.universe.camera.pixel(apparition.coo)
                    apparition_pixel = (
                        pixel[0] - apparition_sprite.width // 2,
                        pixel[1] - apparition_sprite.height,
                    )
                    apparition_blit_sequence = (apparition_sprite.surface, apparition_pixel, None, special_flags)

                    if apparition.render_roo not in blit_sequences:
                        blit_sequences[apparition.render_roo] = []
                    blit_sequences[apparition.render_roo].insert(0, apparition_blit_sequence)

            tile = self.universe.at((x, y))
            if tile == None:
                continue
        
            if tile.roo not in blit_sequences:
                blit_sequences[tile.roo] = []

            diff = (x - stt[0], y - stt[1])
            pixel = (pxl[0] + (diff[0] - diff[1]) * (TILE_WIDTH // 2), pxl[1] + (diff[0] + diff[1]) * (SLATE_HEIGHT // 2))

            lwall_pixel = (
                pixel[0] - (TILE_WIDTH // 2),
                pixel[1] + (SLATE_HEIGHT // 2),
            )
            lwall_sprite = self.sprites.get(tile.lwall)
            if lwall_sprite:
                blit_sequence = (lwall_sprite.surface, lwall_pixel, None, special_flags)
                blit_sequences[tile.roo].insert(0, blit_sequence)

            rwall_pixel = (pixel[0], pixel[1] + (SLATE_HEIGHT // 2))
            rwall_sprite = self.sprites.get(tile.rwall)
            if rwall_sprite:
                blit_sequence = (rwall_sprite.surface, rwall_pixel, None, special_flags)
                blit_sequences[tile.roo].insert(0, blit_sequence)

            slate_pixel = (pixel[0] - (TILE_WIDTH // 2), pixel[1])
            slate_sprite = self.sprites.get(tile.slate)
            if slate_sprite:
                blit_sequence = (slate_sprite.surface, slate_pixel, None, special_flags)
                blit_sequences[tile.roo].insert(0, blit_sequence)

        for (x, y) in coords:
            if (x, y) not in blit_sequences:
                continue
            render_screen.blits(blit_sequences[(x, y)], doreturn=False)

    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        self.render_background(render_screen, special_flags)
        self.render_universe(render_screen, special_flags)

    def update(self, ticks: int) -> None:
        if self.paused:
            return

        self.sprites.update(ticks)
        self.universe.update(ticks)