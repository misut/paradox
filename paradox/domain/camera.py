from pydantic import Field, validator

from paradox.domain.apparition import Apparition
from paradox.domain.base import Direction, Updatable
from paradox.domain.constants import *


class Camera(Updatable):
    coo: tuple[int, int]

    attached: Apparition | None

    sight: int = Field(default=15)
    zoom: float = Field(default=1.0)

    direction: Direction = Field(default=Direction.SOUTH)
    velocity: float = Field(default=0.0)
    velocity_limit: float = Field(default=11.0)
    acceleration: float = Field(default=0.0)
    move_power: float = Field(default=100.0)

    @validator("sight")
    def validate_sight(cls, sight: int) -> int:
        if sight <= 0:
            raise Exception()
        if sight > SIGHT_LIMIT:
            raise Exception()
        return sight

    @validator("zoom")
    def validate_zoom(cls, zoom: float) -> float:
        if zoom <= 0.0:
            raise Exception()
        if zoom > 2.0:
            raise Exception()
        return zoom

    @property
    def at(self) -> tuple[int, int]:
        return (int(self.coo[0]), int(self.coo[1]))

    def accelerate(self, secs: float) -> None:
        if self.acceleration == 0.0:
            return

        self.velocity += self.acceleration * secs
        self.velocity = min(self.velocity, self.velocity_limit)

    def move(self, secs: float) -> None:
        if self.velocity == 0.0:
            return

        x, y = self.coo
        x += self.direction.vector[0] * self.velocity * secs
        y += self.direction.vector[1] * self.velocity * secs
        self.coo = (x, y)

    def look_at(self, coo: tuple[float, float], zoom: float = 1.0) -> None:
        self.coo = coo
        self.zoom = zoom

    def pixel(self, coo: tuple[float, float], viewport: tuple[int, int] = (640, 360)) -> tuple[int, int]:
        diff = (coo[0] - self.coo[0], coo[1] - self.coo[1])
        return (
            viewport[0] // 2 + (TILE_WIDTH // 2) * (diff[0] - diff[1]),
            viewport[1] // 2 + (SLATE_HEIGHT // 2) * (diff[0] + diff[1]),
        )

    def update(self, ticks: int) -> None:
        if self.attached:
            self.look_at(self.attached.coo)
            return

        secs = ticks / 1000
        self.accelerate(secs)
        self.move(secs)
