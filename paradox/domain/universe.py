from abc import ABC

from pydantic import Field

from paradox.domain.apparition import Apparition
from paradox.domain.base import Entity, ValueObject
from paradox.domain.camera import Camera
from paradox.domain.sprite import SpriteTag

EMPTY_ARRAY = [0 for _ in range(128)]


class Tile(ValueObject):
    coo: tuple[int, int]
    roo: tuple[int, int]

    lwall: SpriteTag | None
    rwall: SpriteTag | None
    slate: SpriteTag | None


class Universe(Entity):
    apparitions: list[Apparition] = Field(default=[])
    camera: Camera = Field(default=Camera(coo=(0.0, 0.0), viewport=(640, 360)))
    mapping: dict[tuple[int, int], Tile] = Field(default={})

    def at(self, coo: tuple[float, float]) -> Tile:
        x, y = map(int, coo)
        return self.mapping.get((x, y), Tile(coo=(x, y), roo=(x, y)))

    def place(self, apprition: Apparition) -> None:
        self.apparitions.append(apprition)


class UniverseRepository(ABC):
    def get(self, name: str) -> Universe | None:
        ...
