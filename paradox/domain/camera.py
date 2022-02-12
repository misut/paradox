from pydantic import Field, validator

from paradox.domain.apparition import Apparition
from paradox.domain.base import Entity
from paradox.domain.constants import *

MAX_SIGHT = 100


class Camera(Entity):
    coo: tuple[float, float]  # Coordinate of tile which is centered at viewport
    viewport: tuple[int, int]

    attached: Apparition | None

    sight: int = Field(default=10)
    zoom: float = Field(default=1.0)

    @validator("sight")
    def validate_sight(cls, sight: int) -> int:
        if sight <= 0:
            raise Exception()
        if sight > MAX_SIGHT:
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

    def look_at(self, coo: tuple[float, float, float], zoom: float = 1.0) -> None:
        self.coo = coo
        self.zoom = zoom

    def pixel(self, coo: tuple[float, float]) -> tuple[int, int]:
        diff = (coo[0] - self.coo[0], coo[1] - self.coo[1])
        return (
            self.viewport[0] // 2 + WALL_WIDTH * (diff[0] - diff[1]),
            self.viewport[1] // 2 + (SLATE_HEIGHT // 2) * (diff[0] + diff[1]),
        )
