from pydantic import Field
import pygame

from paradox.domain.base import ValueObject


class Palette(ValueObject):
    special_flags: int = Field(default=pygame.BLEND_ALPHA_SDL2)


class IntroPalette(Palette):
    ...
