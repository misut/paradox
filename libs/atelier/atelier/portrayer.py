from __future__ import annotations

from collections.abc import Callable
from typing import Any, Concatenate, ParamSpec

from pydantic import BaseModel, Field

from atelier.errors import PaletteNotOccupiedError

Params = ParamSpec("Params")
PortrayingMethod = Callable[Concatenate[Any, Params], None]


class Portrayer(BaseModel):
    mapping: dict[type[Any], PortrayingMethod] = Field(default={})

    def invite(self, portrayer: Portrayer) -> None:
        self.mapping.update(portrayer.mapping)

    def occupy(self) -> Callable[[PortrayingMethod], PortrayingMethod]:
        def decorator(portraying_method: PortrayingMethod) -> PortrayingMethod:
            params = list(portraying_method.__annotations__)
            scene_type = portraying_method.__annotations__[params[0]]
            self.mapping[scene_type] = portraying_method
            return portraying_method
        return decorator

    def portray(self, palette: Any) -> None:
        palette_type = type(palette)
        if palette_type not in self.mapping:
            raise PaletteNotOccupiedError(f"{palette}")

        portraying_method = self.mapping[palette_type]
        portraying_method(palette)
