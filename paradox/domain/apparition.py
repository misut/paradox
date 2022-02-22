from enum import Enum, unique

from pydantic import Field

from paradox.domain.base import Direction, Entity, Placeable, Updatable, ValueObject
from paradox.domain.sprite import Sprite, SpriteTag


@unique
class ApparitionStatus(str, Enum):
    ATTACKING: str = "attacking"
    FLOATING: str = "floating"
    STANDING: str = "standing"
    RUNNING: str = "running"

    ATTACKED: str = "attacked"
    STOPPED: str = "stopped"


ApparitionSpriteTags = dict[ApparitionStatus, dict[Direction, SpriteTag]]


@unique
class ApparitionTag(str, Enum):
    PLAYER: str = "player"


class ApparitionStats(ValueObject):
    ...


class ApparitionAsset(ValueObject):
    tag: ApparitionTag
    sprites: ApparitionSpriteTags
    stats: ApparitionStats


class Apparition(Entity, Placeable, Updatable):
    sprites: dict[Direction, Sprite]
    tag: ApparitionTag

    jump_count: int = Field(default=0)
    jump_limit: int = Field(default=0)
    jump_velocity: float = Field(default=20.0)

    status: ApparitionStatus = Field(default=ApparitionStatus.STANDING)

    @property
    def sprite(self) -> Sprite:
        return self.sprites[self.direction]

    @property
    def jumping(self) -> bool:
        return self.fall_velocity < 0.0

    def can_jump(self) -> None:
        if self.jump_count >= self.jump_limit:
            return False
        return True

    def jump(self) -> None:
        if not self.can_jump():
            return None

        self.jump_count += 1
        self.fall_velocity = -self.jump_velocity

    def load(self) -> None:
        super().load()

        self.jump_count = 0


apparition_assets: dict[ApparitionTag, ApparitionAsset] = {}
