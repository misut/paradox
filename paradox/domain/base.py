from collections.abc import Sequence
from numbers import Number
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

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
