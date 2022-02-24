import json
from pathlib import Path

import pygame
from pydantic import BaseModel, Field
from pygame import Rect, Surface

from paradox.domain import (
    Sprite,
    SpriteAsset,
    SpriteRepository,
    SpriteTag,
    sprite_assets,
)


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


class FileSpriteRepository(SpriteRepository):
    sprites: dict[SpriteTag, Sprite] = {}
    sprites_path: Path

    def __init__(self, sprites_path: Path) -> None:
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
        sprite_assets[sprite_info.tag] = sprite_asset
        return sprite_asset.sprite(sprite_info.cycletime)

    def load_sprites(self) -> None:
        json_path = self.sprites_path.joinpath("sprites.json")
        with json_path.open(mode="rt", encoding="utf-8") as stream:
            sprite_info_dicts = json.load(stream)

        for sprite_info_dict in sprite_info_dicts:
            sprite_info = SpriteInfo.parse_obj(sprite_info_dict)
            self.sprites[sprite_info.tag] = self.from_info(sprite_info)

    def copy(self, tag: SpriteTag) -> Sprite | None:
        original_sprite = self.sprites.get(tag, None)
        if original_sprite == None:
            return None

        return original_sprite.copy()

    def get(self, tag: SpriteTag) -> Sprite | None:
        return self.sprites.get(tag, None)

    def update(self, ticks: int) -> None:
        for sprite in self.sprites.values():
            sprite.update(ticks)
