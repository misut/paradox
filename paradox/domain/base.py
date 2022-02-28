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
class Direction(str, Enum):
    def __init__(self, dir: str) -> None:
        match dir:
            case "none":
                self.direction = (0, 0)
            case "north":
                self.direction = (-1, -1)
            case "south":
                self.direction = (1, 1)
            case "east":
                self.direction = (1, -1)
            case "west":
                self.direction = (-1, 1)
            case "northeast":
                self.direction = (0, -2)
            case "northwest":
                self.direction = (-2, 0)
            case "southeast":
                self.direction = (2, 0)
            case "southwest":
                self.direction = (0, 2)
            case _:
                raise ValueError(f"Not allowed direction name: {dir}")

    NONE: str = "none"
    NORTH: str = "north"
    SOUTH: str = "south"
    EAST: str = "east"
    WEST: str = "west"
    NORTHEAST: str = "northeast"
    NORTHWEST: str = "northwest"
    SOUTHEAST: str = "southeast"
    SOUTHWEST: str = "southwest"

    @property
    def vector(self) -> tuple[float, float]:
        return _norm(*self.direction)

    @classmethod
    def from_direction(cls, direction: tuple[int, int]) -> Direction:
        for d in cls:
            if d.direction == direction:
                return d
        
        raise ValueError(f"Not allowed direction: {direction}")

    def __add__(self, other: Direction) -> Direction:
        if self == other:
            return self

        return self.from_direction((self.direction[0] + other.direction[0], self.direction[1] + other.direction[1]))

    def __sub__(self, other: Direction) -> Direction:
        return self.from_direction((self.direction[0] - other.direction[0], self.direction[1] - other.direction[1]))


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
