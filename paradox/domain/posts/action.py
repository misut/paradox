from enum import Enum, unique

from pydantic import Field

from paradox.domain.base import ValueObject
from paradox.domain.posts.base import Post


@unique
class Action(str, Enum):
    UP: str = "up"
    DOWN: str = "down"
    LEFT: str = "left"
    RIGHT: str = "right"


@unique
class ActionType(str, Enum):
    PRESSED: str = "pressed"
    PRESSING: str = "pressing"
    RELEASED: str = "released"


class ActionInfo(ValueObject):
    action: Action
    type: ActionType
    duration: int


class ActionPost(Post):
    infos: dict[Action, ActionInfo]
