import pygame
from pydantic import Field

from paradox.domain.base import ValueObject


class Post(ValueObject):
    ...


class QuitPost(Post):
    ...


class TickPost(Post):
    fps: float
    ticks: int

    special_flags: int = Field(default=pygame.BLEND_ALPHA_SDL2)

    def __str__(self) -> str:
        return f"Rendering previous frame has taken {self.ticks} msecs."
