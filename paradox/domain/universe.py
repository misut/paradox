from abc import ABC

from pydantic import Field

from paradox.domain.base import Entity, ValueObject
from paradox.domain.camera import Camera
from paradox.domain.sprite import SpriteTag


class Tile(ValueObject):
    coo: tuple[int, int, int]

    lwall: SpriteTag | None
    rwall: SpriteTag | None
    slate: SpriteTag | None


class Universe(Entity):
    camera: Camera = Field(default=Camera(coo=(0.0, 0.0, 0.0), viewport=(640, 360)))
    mapping: dict[tuple[int, int, int], Tile]

    def at(self, coo: tuple[float, float, float]) -> Tile:
        _coo = tuple(map(int, coo))
        return self.mapping.get(_coo, Tile(coo=_coo))


class UniverseRepository(ABC):
    def get(self, name: str) -> Universe | None:
        ...
