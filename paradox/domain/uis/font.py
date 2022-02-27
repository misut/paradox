from abc import ABC, abstractmethod
from enum import Enum, unique
from pathlib import Path

from pydantic import BaseModel, Field
from pygame.font import Font

FONTS_PATH: Path = Path("assets/fonts")


@unique
class FontFace(str, Enum):
    NotoSans: str = "NotoSansKR-{font_weight}.otf"


@unique
class FontWeight(str, Enum):
    BLACK: str = "Black"
    BOLD: str = "Bold"
    MEDIUM: str = "Medium"
    REGULAR: str = "Regular"
    LIGHT: str = "Light"
    THIN: str = "Thin"


class FontAssetManager(ABC, BaseModel):
    @abstractmethod
    def get(
        self,
        font_face: FontFace,
        font_size: int,
        font_weight: FontWeight = FontWeight.REGULAR,
    ) -> Font:
        ...


class FileFontAssetManager(FontAssetManager):
    font_assets: dict[FontFace, dict[FontWeight, dict[int, Font]]] = Field(default={})
    fonts_path: Path = Field(default=Path("assets/fonts"))

    class Config:
        arbitrary_types_allowed = True

    def initialize(self, fonts_path: Path = Path("assets/fonts")) -> None:
        self.fonts_path = fonts_path

    def get(
        self,
        font_face: FontFace,
        font_size: int,
        font_weight: FontWeight = FontWeight.REGULAR,
    ) -> Font:
        if font_face not in self.font_assets:
            self.font_assets[font_face] = {weight: {} for weight in FontWeight}

        if font_size not in self.font_assets[font_face][font_weight]:
            font_path = font_face.value.format(font_weight=font_weight.value)
            self.font_assets[font_face][font_weight][font_size] = Font(
                self.fonts_path.joinpath(font_path), font_size
            )

        return self.font_assets[font_face][font_weight][font_size]


font_assets = FileFontAssetManager()
