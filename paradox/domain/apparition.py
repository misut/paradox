from enum import Enum, unique

from pydantic import Field

from paradox.domain.base import Direction, Entity, Updatable
from paradox.domain.sprite import SpriteTag


class ApparitionTag(str, Enum):
    PLAYER: str = "player"


class Apparition(Entity, Updatable):
    coo: tuple[float, float]
    dim: tuple[float, float]
    sprite: SpriteTag
    tag: ApparitionTag

    direction: Direction = Field(default=Direction.NORTH)
    velocity: float = Field(default=0.0)

    @property
    def moving(self) -> bool:
        if self.velocity > 0.0:
            return True
        return False

    def move(self, ticks: int) -> None:
        x, y = self.coo
        secs = ticks / 1000
        x += self.direction[0] * self.velocity * secs
        y += self.direction[1] * self.velocity * secs
        self.coo = (x, y)

    def update(self, ticks: int) -> None:
        super().update(ticks)
        
        self.move(ticks)
