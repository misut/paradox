from abc import ABC

from pydantic import Field
from pygame import Surface

from paradox.domain.base import Entity, Renderable, ValueObject
from paradox.domain.camera import Camera
from paradox.domain.sprite import SpriteTag


class Tile(ValueObject):
    coo: tuple[float, float, float]

    lwall: SpriteTag | None
    rwall: SpriteTag | None
    slate: SpriteTag | None


class Universe(Entity, Renderable):
    camera: Camera = Field(default=Camera(coo=(0.0, 0.0, 0.0)))

    def at(self, coo: tuple[float, float, float]) -> Tile:
        raise NotImplementedError

    def render(self, render_screen: Surface, special_flags: int = 0, sight: tuple[int, int, int] = (10, 10, 10)) -> None:
        pass


class UniverseRepository(ABC):
    def get(self, name: str) -> Universe | None:
        ...
