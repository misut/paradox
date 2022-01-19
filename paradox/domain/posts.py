import pygame
from pygame.event import Event

from paradox.domain.base import ValueObject
from paradox.domain.enums import MouseButton


class Post(ValueObject):
    ...


class QuitPost(Post):
    ...


class KeyDownPost(Post):
    code: int

    def __str__(self) -> str:
        return f"Key {self.code} is pressed."


class KeyUpPost(Post):
    code: int

    def __str__(self) -> str:
        return f"Key {self.code} is released."


class MouseButtonDownPost(Post):
    pos: tuple[int, int]
    button: MouseButton
    touch: bool

    def __str__(self) -> str:
        return f"Mouse {self.button} is pressed at {self.pos}"


class MouseButtonUpPost(Post):
    pos: tuple[int, int]
    button: MouseButton
    touch: bool

    def __str__(self) -> str:
        return f"Mouse {self.button} is released at {self.pos}"


class MouseMotionPost(Post):
    pos: tuple[int, int]
    rel: tuple[int, int]
    buttons: list[MouseButton]
    touch: bool

    def __str__(self) -> str:
        return (
            f"Mouse moved to {self.pos} {self.rel} with buttons pressed{self.buttons}"
        )
