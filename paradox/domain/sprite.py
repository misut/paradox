from abc import ABC, abstractmethod
from enum import Enum, unique

from pydantic import Field, validator
from pygame import Surface

from paradox.domain.base import Renderable, Updatable
from paradox.domain.errors import SpriteLoadError


@unique
class SpriteTag(str, Enum):
    NONE: str = "none"

    APPARITION_TEST: str = "apparition:test"

    LWALL_TEST: str = "lwall:test"
    LWALL_GRASS: str = "lwall:grass"

    RWALL_TEST: str = "rwall:test"
    RWALL_GRASS: str = "rwall:grass"

    SLATE_TEST: str = "slate:test"
    SLATE_GRASS: str = "slate:grass"


class Sprite(Renderable, Updatable):
    tag: SpriteTag
    surfaces: list[Surface]
    surface_index: int = Field(default=0)

    cycletime: int = Field(default=100)

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

    def cycle(self) -> None:
        self.surface_index += 1
        if self.surface_index >= len(self.surfaces):
            self.surface_index = 0

    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        render_screen.blit(self.surface, self.pos, None, special_flags)


class SpriteRepository(ABC):
    @abstractmethod
    def get(self, tag: SpriteTag) -> Sprite | None:
        ...

    @abstractmethod
    def update(self, ticks: int) -> None:
        ...
