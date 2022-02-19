from __future__ import annotations

from collections.abc import Sequence
from enum import Enum, unique
from math import floor
from numbers import Number
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator
from pygame import Surface

ID = UUID
generate_id = uuid4


def _norm(*ns: Number) -> Sequence[Number]:
    dist = sum(n ** 2.0 for n in ns) ** (1 / 2)
    if dist == 0.0:
        return tuple(0.0 for _ in ns)
    return tuple(map(lambda n: n / dist, ns))


@unique
class Direction(tuple[int, int], Enum):
    def __init__(self, dir: tuple[int, int]) -> None:
        self.vector = _norm(*dir)

    NONE: tuple[int, int] = (0, 0)
    NORTH: tuple[int, int] = (-1, -1)
    SOUTH: tuple[int, int] = (1, 1)
    EAST: tuple[int, int] = (1, -1)
    WEST: tuple[int, int] = (-1, 1)
    NORTHEAST: tuple[int, int] = (0, -2)
    NORTHWEST: tuple[int, int] = (-2, 0)
    SOUTHEAST: tuple[int, int] = (2, 0)
    SOUTHWEST: tuple[int, int] = (0, 2)

    def __add__(self, other: Direction) -> Direction:
        if self == other:
            return self
        return Direction((self[0] + other[0], self[1] + other[1]))

    def __sub__(self, other: Direction) -> Direction:
        return Direction((self[0] - other[0], self[1] - other[1]))


class ValueObject(BaseModel):
    class Config:
        allow_mutation = False


class Entity(BaseModel):
    id: ID = Field(default_factory=generate_id)
    name: str = Field(default="")


class Renderable(BaseModel):
    pos: tuple[int, int] = Field(default=(0, 0))
    size: tuple[int, int]

    @property
    def left(self) -> int:
        return self.pos[0]

    @property
    def right(self) -> int:
        return self.pos[0] + self.size[0] - 1

    @property
    def top(self) -> int:
        return self.pos[1]

    @property
    def bottom(self) -> int:
        return self.pos[1] + self.size[1] - 1

    @property
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self) -> int:
        return self.size[1]

    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        pass


class Updatable(BaseModel):
    cycletime: int = Field(default=0)  # in millisecond
    hourglass: int = Field(default=0)  # in millisecond

    def cycle(self) -> None:
        pass

    def update(self, ticks: int) -> None:
        if self.cycletime == 0:
            return

        self.hourglass += ticks
        if self.hourglass < self.cycletime:
            return

        self.hourglass -= self.cycletime
        self.cycle()


class Placeable(BaseModel):
    coo: tuple[float, float]
    roo: tuple[float, float]
    dim: tuple[float, float] = Field(default=(0.0, 0.0))

    direction: Direction = Field(default=Direction.SOUTH)
    velocity: float = Field(default=0.0)
    velocity_limit: float = Field(default=11.0)
    acceleration: float = Field(default=0.0)

    foo: tuple[float, float] | None
    fidx: float | None
    fall_velocity: float = Field(default=0.0)
    fall_velocity_limit: float = Field(default=100.0)
    gravity: float = Field(default=0.0)

    def __lt__(self, other: Placeable) -> bool:
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
        self.acceleration = 0.0
        self.direction = Direction.SOUTH
        self.velocity = 0.0
        self.gravity = 0.0
        self.fall_velocity = 0.0

        self.foo = None
        self.fidx = None

    def simulate(self, secs: float) -> Placeable:
        future_placeable = self.copy()
        future_placeable.accelerate(secs)
        future_placeable.move(secs)
        future_placeable.gravitate(secs)
        future_placeable.fall(secs)
        return future_placeable
