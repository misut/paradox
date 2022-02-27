from math import floor

from pydantic import Field, validator

from paradox.domain.apparition import Apparition
from paradox.domain.base import Updatable
from paradox.domain.constants import *


class Camera(Updatable):
    coo: tuple[float, float]
    dst: tuple[float, float] = Field(default=(0.0, 0.0))

    attached: Apparition | None

    sight: int = Field(default=15)
    smooth: float = Field(default=200.0)
    zoom: float = Field(default=1.0)

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
        return (floor(self.coo[0]), floor(self.coo[1]))

    def move(self, delta: tuple[float, float]) -> None:
        x, y = self.dst
        x += delta[0]
        y += delta[1]
        self.dst = (x, y)

    def look_at(self, dst: tuple[float, float], zoom: float = 1.0) -> None:
        self.dst = dst
        self.zoom = zoom

    def pixel(
        self, coo: tuple[float, float], viewport: tuple[int, int] = (640, 360)
    ) -> tuple[int, int]:
        diff = (coo[0] - self.coo[0], coo[1] - self.coo[1])
        return (
            viewport[0] // 2 + (TILE_WIDTH // 2) * (diff[0] - diff[1]),
            viewport[1] // 2 + (SLATE_HEIGHT // 2) * (diff[0] + diff[1]),
        )

    def update(self, ticks: int) -> None:
        if self.attached:
            self.look_at(self.attached.coo)

        if self.coo == self.dst:
            return

        x, y = self.coo
        x += (self.dst[0] - self.coo[0]) * ticks / self.smooth
        y += (self.dst[1] - self.coo[1]) * ticks / self.smooth
        self.coo = (x, y)
