from enum import Enum, unique

from paradox.domain.base import Entity, Placeable
from paradox.domain.sprite import SpriteTag


@unique
class ApparitionTag(str, Enum):
    PLAYER: str = "player"


class Apparition(Entity, Placeable):
    sprite: SpriteTag
    tag: ApparitionTag
