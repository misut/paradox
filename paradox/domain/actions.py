from enum import Enum, unique

from pydantic import Field

from paradox.domain.base import ValueObject


@unique
class ActionType(str, Enum):
    PRESSED: str = "pressed"
    PRESSING: str = "pressing"
    RELEASED: str = "released"


class Action(ValueObject):
    type: ActionType
    duration: int = Field(default=0)  # in milliseconds


class LeftAction(Action):
    ...


class RightAction(Action):
    ...


class UpAction(Action):
    ...


class DownAction(Action):
    ...
