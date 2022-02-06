from enum import Enum, unique


@unique
class MouseButton(int, Enum):
    MOVE: int = 0
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


@unique
class Action(int, Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


@unique
class HorizontalAlignment(str, Enum):
    CENTER: str = "center"
    LEFT: str = "left"
    RIGHT: str = "right"


@unique
class VerticalAlignment(str, Enum):
    BOTTOM: str = "bottom"
    MIDDLE: str = "middle"
    TOP: str = "top"
