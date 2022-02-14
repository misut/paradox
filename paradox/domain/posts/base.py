import pygame
from pydantic import Field

from paradox.domain.action import ActionInfoTable
from paradox.domain.base import ValueObject


class Post(ValueObject):
    ...


class QuitPost(Post):
    ...


class TickPost(Post):
    actions: ActionInfoTable
    fps: float
    ticks: int

    special_flags: int = Field(default=pygame.BLEND_ALPHA_SDL2)

    def __str__(self) -> str:
        return f"Rendering previous frame has taken {self.ticks} msecs."
