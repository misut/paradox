from abc import ABC, abstractmethod
from enum import Enum, unique

from pydantic import Field, validator
from pygame import Surface

from paradox.domain.base import Updatable, ValueObject
from paradox.domain.errors import SpriteLoadError


@unique
class SpriteType(str, Enum):
    APPARITION: str = "apparition"
    LWALL: str = "lwall"
    RWALL: str = "rwall"
    SLATE: str = "slate"


@unique
class SpriteTag(str, Enum):
    def __init__(self, tag: str) -> None:
        splitted = tag.split(":")
        if len(splitted) != 2:
            raise ValueError("Sprite tag should be in a form of 'type:label'")

        self.type = SpriteType(splitted[0])
        self.label = splitted[1]

    APPARITION_TEST: str = "apparition:test"
    APPARITION_SHRIMP_S: str = "apparition:shrimp_s"
    APPARITION_SLIME: str = "apparition:slime"

    LWALL_TEST: str = "lwall:test"
    LWALL_GRASS: str = "lwall:grass"

    RWALL_TEST: str = "rwall:test"
    RWALL_GRASS: str = "rwall:grass"

    SLATE_TEST: str = "slate:test"
    SLATE_GRASS: str = "slate:grass"


class SpriteAsset(ValueObject):
    tag: SpriteTag
    size: tuple[int, int]
    surfaces: list[Surface]

    class Config:
        arbitrary_types_allowed = True

    @validator("surfaces")
    def validate_surfaces(cls, surfaces: list[Surface]) -> list[Surface]:
        if not surfaces:
            raise SpriteLoadError("Sprite must have at least a surface.")
        return surfaces

    def __getitem__(self, idx: int) -> Surface:
        return self.surfaces[idx]

    def __len__(self) -> int:
        return len(self.surfaces)

    def sprite(self, cycletime: int = 100) -> "Sprite":
        return Sprite(
            tag=self.tag,
            size=self.size,
            cycletime=cycletime,
            surface_index=0,
            surface_limit=len(self),
        )


class Sprite(Updatable):
    tag: SpriteTag
    size: tuple[int, int]

    cycletime: int = Field(default=100)
    surface_index: int = Field(default=0)
    surface_limit: int = Field(default=0)

    class Config:
        arbitrary_types_allowed = True

    @property
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self) -> int:
        return self.size[1]

    @property
    def surface(self) -> Surface:
        global sprite_assets
        return sprite_assets[self.tag][self.surface_index]

    def cycle(self) -> None:
        self.surface_index += 1
        if self.surface_index >= self.surface_limit:
            self.surface_index = 0

    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        render_screen.blit(self.surface, self.pos, None, special_flags)


class SpriteRepository(ABC):
    @abstractmethod
    def copy(self, tag: SpriteTag) -> Sprite | None:
        ...

    @abstractmethod
    def get(self, tag: SpriteTag) -> Sprite | None:
        ...

    @abstractmethod
    def update(self, ticks: int) -> None:
        ...


sprite_assets: dict[SpriteTag, SpriteAsset] = {}
