from pydantic import Field, validator

from paradox.domain.base import Entity


class Camera(Entity):
    coo: tuple[float, float, float]
    zoom: float = Field(default=1.0)

    @validator("zoom")
    def validate_zoom(cls, zoom: float) -> float:
        if zoom <= 0.0:
            raise Exception()
        if zoom > 2.0:
            raise Exception()
        return zoom

    @property
    def sight(self) -> tuple[int, int, int]:
        return (10, 10, 10)

    def look_at(self, coo: tuple[float, float, float], zoom: float = 1.0) -> None:
        self.coo = coo
        self.zoom = zoom
