from __future__ import annotations

from typing import Callable

from pydantic import BaseModel, Field
from pygame import Surface

from atelier.palette import Palette

PortrayingMethod = Callable[[Palette, Surface, int], None]


class Portrayer(BaseModel):
    mapping: dict[type[Palette], PortrayingMethod] = Field(default={})

    def invite(self, portrayer: Portrayer) -> None:
        self.mapping.update(portrayer.mapping)

    def occupy(self) -> Callable[[PortrayingMethod], PortrayingMethod]:
        def decorator(portraying_method: PortrayingMethod) -> PortrayingMethod:
            params = list(portraying_method.__annotations__)
            scene_type = portraying_method.__annotations__[params[0]]
            self.mapping[scene_type] = portraying_method
            return portraying_method
        return decorator

    def portray(self, palette: Palette, portrait: Surface, special_flags: int = 0) -> None:
        palette_type = type(palette)
        if palette_type not in self.mapping:
            raise Exception(f"Not supported type of a palette: {palette_type.__name__}")

        portraying_method = self.mapping[palette_type]
        portraying_method(palette, portrait, special_flags)
