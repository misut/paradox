from typing import Optional

from postoffice import Post
from pygame.event import Event
import pygame

from paradox.domain.enums import MouseButton


def propagate_event_to_post(event: Event) -> Optional[Post]:
    match event.type:
        case pygame.KEYDOWN:
            post = KeyDownPost(code=event.scancode)
        case pygame.KEYUP:
            post = KeyUpPost(code=event.scancode)
        case pygame.MOUSEBUTTONDOWN:
            post = MouseButtonDownPost(pos=event.pos, button=event.button, touch=event.touch)
        case pygame.MOUSEBUTTONUP:
            post = MouseButtonUpPost(pos=event.pos, button=event.button, touch=event.touch)
        case pygame.MOUSEMOTION:
            post = MouseMotionPost(pos=event.pos, rel=event.rel, buttons=event.buttons, touch=event.touch)
        case pygame.QUIT:
            post = QuitPost()
        case _:
            return None
    
    return post


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
        return f"Mouse moved to {self.pos} {self.rel} with buttons pressed{self.buttons}"
