import json
from pathlib import Path

import pygame
from pydantic import BaseModel
from pygame import Rect, Surface

from paradox.domain import Sprite, SpriteRepository, SpriteTag


class SpriteFile(BaseModel):
    tag_name: str
    path: Path
    size: tuple[int, int]

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

    def from_file(self, sprite_file: SpriteFile) -> Sprite:
        file_path = self.sprites_path.joinpath(sprite_file.path)
        bulk_surface = pygame.image.load(file_path)

        surfaces = []
        for coef in range(bulk_surface.get_width() // sprite_file.width):
            surface = Surface(sprite_file.size, pygame.SRCALPHA)
            rect = Rect(
                sprite_file.width * coef, 0, sprite_file.width, sprite_file.height
            )
            surface.blit(bulk_surface, (0, 0), rect, pygame.BLEND_ALPHA_SDL2)
            surfaces.append(surface)

        return Sprite(
            pos=(0, 0), size=sprite_file.size, tag=SpriteTag[sprite_file.tag_name], surfaces=surfaces
        )

    def load_sprites(self) -> None:
        json_path = self.sprites_path.joinpath("sprites.json")
        with json_path.open(mode="rt", encoding="utf-8") as stream:
            sprite_file_dicts = json.load(stream)

        for sprite_file_dict in sprite_file_dicts:
            sprite_file = SpriteFile.parse_obj(sprite_file_dict)
            sprite_tag = SpriteTag[sprite_file.tag_name]
            self.sprites[sprite_tag] = self.from_file(sprite_file)

    def get(self, tag: SpriteTag) -> Sprite | None:
        return self.sprites.get(tag, None)

    def update(self, ticks: int) -> None:
        for sprite in self.sprites.values():
            sprite.update(ticks)
