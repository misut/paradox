from __future__ import annotations

from collections.abc import Sequence
from enum import Enum, unique
from numbers import Number
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
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


class Placeable(Updatable):
    coo: tuple[float, float]
    roo: tuple[float, float]
    dim: tuple[float, float] = Field(default=(0.0, 0.0))

    direction: Direction = Field(default=Direction.SOUTH)
    velocity: float = Field(default=0.0)
    velocity_limit: float = Field(default=5.0)
    acceleration: float = Field(default=0.0)
    # TODO: Not used
    gravity: float = Field(default=9.8)

    @property
    def moving(self) -> bool:
        if self.velocity > 0.0:
            return True
        return False

    def accelerate(self, secs: float) -> None:
        if self.acceleration == 0.0:
            return 

        self.velocity += self.acceleration * secs
        if self.velocity < 0.0:
            self.velocity = 0.0
        else:
            self.velocity = min(self.velocity, self.velocity_limit)

    def move(self, secs: float) -> None:
        if self.velocity == 0.0:
            return

        x, y = self.coo
        x += self.direction.vector[0] * self.velocity * secs
        y += self.direction.vector[1] * self.velocity * secs
        self.coo = (x, y)

    def update(self, ticks: int) -> None:
        super().update(ticks)

        secs = ticks / 1000
        self.accelerate(secs)
        self.move(secs)
