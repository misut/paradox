from __future__ import annotations

from abc import ABC
from enum import Enum, unique
from math import floor
from typing import Any

from pydantic import BaseModel, Field, validator
from pygame import Surface

from paradox.domain.base import Direction, Entity, Updatable, ValueObject
from paradox.domain.sprite import Sprite, SpriteTag


@unique
class ApparitionStatus(str, Enum):
    ATTACKING: str = "attacking"
    RUNNING: str = "running"
    FLOATING: str = "floating"
    STANDING: str = "standing"

    ATTACKED: str = "attacked"
    STOPPED: str = "stopped"


ApparitionSpriteTags = dict[ApparitionStatus, dict[Direction, SpriteTag]]
ApparitionSprite = dict[ApparitionStatus, dict[Direction, Sprite]]
_DEFAULT_SPRITE = {
    status: {direction: SpriteTag.APPARITION_TEST for direction in Direction}
    for status in ApparitionStatus
}


@unique
class ApparitionTag(str, Enum):
    def __init__(self, tag: str) -> None:
        splitted = tag.split(":")
        if len(splitted) != 2:
            raise ValueError("Apparition tag should be in a form of 'type:label'")

        self.type = splitted[0]
        self.label = splitted[1]

    PLAYER: str = "character:player"


class ApparitionStats(ValueObject):
    ...


class ApparitionAsset(ValueObject):
    tag: ApparitionTag
    sprites: ApparitionSpriteTags
    stats: ApparitionStats


class Apparition(Entity, Updatable):
    tag: ApparitionTag
    coo: tuple[float, float]
    roo: tuple[float, float]
    dim: tuple[float, float]

    sprites: ApparitionSprite = Field(default=_DEFAULT_SPRITE)
    status: ApparitionStatus = Field(default=ApparitionStatus.STANDING)

    direction: Direction = Field(default=Direction.SOUTH)
    move_power: float = Field(default=30.0)
    velocity: float = Field(default=0.0)
    velocity_limit: float = Field(default=11.0)
    acceleration: float = Field(default=0.0)

    foo: tuple[float, float] | None
    fidx: float | None
    fall_power: float = Field(default=98.0)
    fall_velocity: float = Field(default=0.0)
    fall_velocity_limit: float = Field(default=100.0)
    gravity: float = Field(default=0.0)

    def __lt__(self, other: Apparition) -> bool:
        return sum(self.roo) < sum(other.roo)

    @validator("roo")
    def validate_roo(
        cls, roo: tuple[float, float], values: dict[str, Any]
    ) -> tuple[float, float]:
        coo = values.get("coo")
        if roo[0] - coo[0] == roo[1] - coo[1]:
            return roo
        raise ValueError("wow")

    @property
    def falling(self) -> bool:
        if self.fall_velocity == 0.0:
            return False
        return True

    @property
    def moving(self) -> bool:
        if self.velocity == 0.0:
            return False
        return True

    @property
    def render_roo(self) -> tuple[int, int]:
        left = self.roo[1] - floor(self.roo[1])
        right = self.roo[0] - floor(self.roo[0])
        if left > 0.9:
            return tuple(map(floor, (self.roo[0], self.roo[1] + self.dim[0])))
        elif right > 0.9:
            return tuple(map(floor, (self.roo[0] + self.dim[0], self.roo[1])))
        return tuple(map(floor, (self.roo[0], self.roo[1])))

    @property
    def sprite(self) -> Sprite:
        return self.sprites[self.status][self.direction]

    @property
    def surface(self) -> Surface:
        return self.sprite.surface

    @property
    def zidx(self) -> float:
        return self.roo[0] - self.coo[0]

    def accelerate(self, secs: float) -> None:
        if self.acceleration == 0.0:
            return

        self.velocity += self.acceleration * secs
        self.velocity = min(self.velocity, self.velocity_limit)

    def gravitate(self, secs: float) -> None:
        if self.gravity == 0.0:
            return

        self.fall_velocity += self.gravity * secs
        self.fall_velocity = min(self.fall_velocity, self.fall_velocity_limit)

    def fall(self, secs: float) -> None:
        if self.fall_velocity == 0.0:
            return

        x, y = self.coo
        x += Direction.SOUTH.vector[0] * self.fall_velocity * secs
        y += Direction.SOUTH.vector[1] * self.fall_velocity * secs
        self.coo = (x, y)

    def move(self, secs: float) -> None:
        if self.velocity == 0.0:
            return

        x, y = self.coo
        zidx = self.zidx
        x += self.direction.vector[0] * self.velocity * secs
        y += self.direction.vector[1] * self.velocity * secs
        self.coo = (x, y)
        self.roo = (x + zidx, y + zidx)

    def save(self, coo: tuple[int, int], zidx: int) -> None:
        center_coo = (coo[0] + 0.5, coo[1] + 0.5)

        self.foo = center_coo
        self.fidx = zidx

    def load(self) -> None:
        if self.foo == None or self.fidx == None:
            return

        self.coo = self.foo
        self.roo = (self.foo[0] + self.fidx, self.foo[1] + self.fidx)
        self.direction = Direction.SOUTH
        self.velocity = 0.0
        self.acceleration = 0.0

        self.foo = None
        self.fidx = None
        self.fall_velocity = 0.0
        self.gravity = 0.0

    def simulate(self, secs: float) -> Apparition:
        future_placeable = self.copy()

        future_placeable.accelerate(secs)
        future_placeable.move(secs)

        future_placeable.gravitate(secs)
        future_placeable.fall(secs)

        return future_placeable


class ApparitionAssetManager(ABC, BaseModel):
    ...


apparition_assets: dict[ApparitionTag, ApparitionAsset] = {}
