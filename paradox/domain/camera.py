from pydantic import Field, validator

from paradox.domain.base import Entity


class Camera(Entity):
    coo: tuple[float, float, float]  # Coordinate of tile which is centered at viewport
    viewport: tuple[int, int]
    zoom: float = Field(default=1.0)

    @validator("zoom")
    def validate_zoom(cls, zoom: float) -> float:
        if zoom <= 0.0:
            raise Exception()
        if zoom > 2.0:
            raise Exception()
        return zoom

    @property
    def at(self) -> tuple[int, int, int]:
        return (int(self.coo[0]), int(self.coo[1]), int(self.coo[2]))

    @property
    def sight(self) -> tuple[int, int, int]:
        return (5, 5, 5)

    def look_at(self, coo: tuple[float, float, float], zoom: float = 1.0) -> None:
        self.coo = coo
        self.zoom = zoom
    
    def pixel(self, coo: tuple[float, float, float]) -> tuple[int, int]:
        diff = (coo[0] - self.coo[0], coo[1] - self.coo[1], coo[2] - self.coo[2])
        return (
            self.viewport[0] // 2 + 29 * (diff[0] - diff[1]),
            self.viewport[1] // 2 + 16 * (diff[0] + diff[1]) - 33 * diff[2]
        )
