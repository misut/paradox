import json
from abc import ABC, abstractmethod
from enum import Enum, unique
from pathlib import Path

import pygame
from pydantic import BaseModel, Field, validator
from pygame import Rect, Surface

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
        return sprite_assets.surface(self.tag, self.surface_index)

    def cycle(self) -> None:
        self.surface_index += 1
        if self.surface_index >= self.surface_limit:
            self.surface_index = 0

    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        render_screen.blit(self.surface, self.pos, None, special_flags)


class SpriteAssetManager(ABC, BaseModel):
    @abstractmethod
    def copy(self, tag: SpriteTag) -> Sprite | None:
        ...

    @abstractmethod
    def get(self, tag: SpriteTag) -> Sprite | None:
        ...

    @abstractmethod
    def surface(self, tag: SpriteTag, surface_index: int) -> Surface | None:
        ...

    @abstractmethod
    def update(self, ticks: int) -> None:
        ...


class SpriteInfo(BaseModel):
    tag: str
    path: Path
    size: tuple[int, int]

    cycletime: int = Field(default=100)

    @property
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self) -> int:
        return self.size[1]


class FileSpriteAssetManager(SpriteAssetManager):
    sprite_assets: dict[SpriteTag, SpriteAsset] = Field(default={})
    sprites: dict[SpriteTag, Sprite] = Field(default={})
    sprites_path: Path = Field(default=Path("assets/sprites"))

    def initialize(self, sprites_path: Path = Path("assets/sprites")) -> None:
        self.sprite_assets.clear()
        self.sprites.clear()
        self.sprites_path = sprites_path
        self.load_sprites()

    def from_info(self, sprite_info: SpriteInfo) -> Sprite:
        file_path = self.sprites_path.joinpath(sprite_info.path)
        bulk_surface = pygame.image.load(file_path)

        surfaces = []
        for coef in range(bulk_surface.get_width() // sprite_info.width):
            surface = Surface(sprite_info.size, pygame.SRCALPHA)
            rect = Rect(
                sprite_info.width * coef, 0, sprite_info.width, sprite_info.height
            )
            surface.blit(bulk_surface, (0, 0), rect, pygame.BLEND_ALPHA_SDL2)
            surfaces.append(surface)

        sprite_asset = SpriteAsset(
            tag=sprite_info.tag, size=sprite_info.size, surfaces=surfaces
        )
        self.sprite_assets[sprite_info.tag] = sprite_asset
        return sprite_asset.sprite(sprite_info.cycletime)
        
    def load_sprites(self) -> None:
        json_path = self.sprites_path.joinpath("sprites.json")
        with json_path.open(mode="rt", encoding="utf-8") as stream:
            sprite_info_dicts = json.load(stream)

        for sprite_info_dict in sprite_info_dicts:
            sprite_info = SpriteInfo.parse_obj(sprite_info_dict)
            self.sprites[sprite_info.tag] = self.from_info(sprite_info)

    def copy(self, tag: SpriteTag) -> Sprite | None:
        if tag not in self.sprite_assets:
            return None
        return self.sprite_assets[tag].sprite()

    def get(self, tag: SpriteTag) -> Sprite | None:
        return self.sprites.get(tag, None)

    def surface(self, tag: SpriteTag, surface_index: int) -> Surface | None:
        if tag not in self.sprite_assets:
            return None
        return self.sprite_assets[tag][surface_index]

    def update(self, ticks: int) -> None:
        for sprite in self.sprites.values():
            sprite.update(ticks)


sprite_assets = FileSpriteAssetManager()
