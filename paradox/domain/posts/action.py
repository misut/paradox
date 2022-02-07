from enum import Enum, unique

from pydantic import Field

from paradox.domain.posts.base import Post


@unique
class Action(str, Enum):
    LEFT: str = "left"
    RIGHT: str = "right"
    UP: str = "up"
    DOWN: str = "down"


@unique
class ActionType(str, Enum):
    PRESSED: str = "pressed"
    PRESSING: str = "pressing"
    RELEASED: str = "released"


class ActionPost(Post):
    action: Action
    type: ActionType

    duration: int = Field(default=0)
