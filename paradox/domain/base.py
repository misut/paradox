from collections.abc import Sequence
from enum import Enum, unique
from numbers import Number
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from pygame import Surface

ID = UUID
generate_id = uuid4


def _dist(num1: Number, num2: Number) -> float:
    return (num1 ** 2 - num2 ** 2) ** (1 / 2)


def dist(pos1: Sequence[Number], pos2: Sequence[Number]) -> float:
    return sum(map(_dist, zip(pos1, pos2)))


@unique
class Direction(tuple[float, float], Enum):
    NORTH: tuple[float, float] = (-(1 / 2) ** (1 / 2), -(1 / 2) ** (1 / 2))
    SOUTH: tuple[float, float] = ((1 / 2) ** (1 / 2), (1 / 2) ** (1 / 2))
    EAST: tuple[float, float] = ((1 / 2) ** (1 / 2), -(1 / 2) ** (1 / 2))
    WEST: tuple[float, float] = (-(1 / 2) ** (1 / 2), (1 / 2) ** (1 / 2))
    NORTHEAST: tuple[float, float] = (0.0, -1.0)
    NORTHWEST: tuple[float, float] = (-1.0, 0.0)
    SOUTHEAST: tuple[float, float] = (1.0, 0.0)
    SOUTHWEST: tuple[float, float] = (0.0, 1.0)


class ValueObject(BaseModel):
    class Config:
        allow_mutation = False


class Entity(BaseModel):
    id: ID = Field(default_factory=generate_id)
    name: str = Field(default="")


class Renderable(BaseModel):
    pos: tuple[int, int] = (0, 0)
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
