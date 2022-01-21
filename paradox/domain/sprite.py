from abc import ABC
from enum import Enum, unique
from typing import Any

from pydantic import Field, validator
from pygame import Surface

from paradox.domain.base import Renderable, Updatable
from paradox.domain.errors import SpriteLoadError


@unique
class SpriteTag(str, Enum):
    LWALL_TEST: str = "lwall:test"
    RWALL_TEST: str = "rwall:test"
    SLATE_TEST: str = "slate:test"


class Sprite(Renderable, Updatable):
    tag: SpriteTag
    surfaces: list[Surface]
    surface_index: int = Field(default=0)
    surface_update_msec: int = Field(default=1000)

    class Config:
        arbitrary_types_allowed = True

    @validator("surfaces")
    def validate_surfaces(cls, surfaces: list[Surface]) -> list[Surface]:
        if not surfaces:
            raise SpriteLoadError("Sprite must have at least a surface.")
        return surfaces

    @property
    def surface(self) -> Surface:
        return self.surfaces[self.surface_index]

    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        super().render(render_screen, special_flags)

        render_screen.blit(self.surface, self.pos, None, special_flags)

    def update(self, ticks: int) -> None:
        super().update(ticks)

        while self.hourglass > self.surface_update_msec:
            self.hourglass -= self.surface_update_msec
            self.surface_index += 1
            if self.surface_index == len(self.surfaces):
                self.surface_index = 0


class SpriteRepository(ABC):
    def get(self, tag: SpriteTag) -> Sprite:
        ...
