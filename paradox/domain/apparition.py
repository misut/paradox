from enum import Enum, unique

from pydantic import Field

from paradox.domain.base import Entity, Placeable, Updatable
from paradox.domain.sprite import SpriteTag


@unique
class ApparitionTag(str, Enum):
    PLAYER: str = "player"


class Apparition(Entity, Placeable, Updatable):
    sprite: SpriteTag
    tag: ApparitionTag

    fall_power: float = Field(default=98.0)
    move_power: float = Field(default=30.0)

    jump_count: int = Field(default=0)
    jump_count_limit: int = Field(default=0)
    jump_velocity: float = Field(default=20.0)
    

    @property
    def jumping(self) -> bool:
        return self.fall_velocity < 0.0

    def can_jump(self) -> None:
        if self.jump_count >= self.jump_count_limit:
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
