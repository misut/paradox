import pygame
from pydantic import Field

from paradox.domain.base import ValueObject


class Palette(ValueObject):
    special_flags: int = Field(default=pygame.BLEND_ALPHA_SDL2)


class IntroPalette(Palette):
    ...
