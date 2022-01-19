from collections.abc import Sequence
from numbers import Number
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from pygame import Surface

generate_uuid = uuid4


def _dist(num1: Number, num2: Number) -> float:
    return (num1 ** 2 - num2 ** 2) ** (1 / 2)


def dist(pos1: Sequence[Number], pos2: Sequence[Number]) -> float:
    return sum(map(_dist, zip(pos1, pos2)))


class ValueObject(BaseModel):
    class Config:
        allow_mutation = False

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)


class Entity(BaseModel):
    id: UUID = Field(default_factory=generate_uuid)
    name: str = Field(default="")

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)


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
    hourglass: int = Field(default=0)  # in millisecond

    def update(self, ticks: int) -> None:
        self.hourglass += ticks
