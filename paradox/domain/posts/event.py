from enum import Enum, unique

from paradox.domain.posts.base import Post


@unique
class EventType(str, Enum):
    DOWN: str = "down"
    UP: str = "up"


class EventPost(Post):
    type: EventType


class KeyEventPost(EventPost):
    code: int


@unique
class MouseButton(int, Enum):
    MOTION: int = 0
    LEFT: int = 1
    MIDDLE: int = 2
    RIGHT: int = 3
    SCROLL_UP: int = 4
    SCROLL_DOWN: int = 5
    BUTTON6: int = 6
    BUTTON7: int = 7
    BUTTON8: int = 8
    BUTTON9: int = 9
    BUTTON10: int = 10


class MouseEventPost(EventPost):
    pos: tuple[int, int]
    button: MouseButton


class MouseMotionPost(Post):
    pos: tuple[int, int]
    rel: tuple[int, int]
    buttons: list[MouseButton]
