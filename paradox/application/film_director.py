from __future__ import annotations

from collections.abc import Callable

from pydantic import BaseModel, Field

from paradox.application.ui_manager import UIManager
from paradox.application.universe_simulator import UniverseSimulator
from paradox.domain import Post, SceneNo

Scene = Callable[[UIManager, UniverseSimulator], list[Post]]


class FilmDirector(BaseModel):
    reel: dict[SceneNo, Scene] = Field(default={})

    def collaborate(self, film_director: FilmDirector) -> None:
        self.reel.update(film_director.reel)

    def take(self, scene_no: SceneNo) -> Callable[[Scene], Scene]:
        def decorator(scene: Scene) -> Scene:
            self.reel[scene_no] = scene
            return scene

        return decorator

    def shoot(
        self,
        scene_no: SceneNo,
        ui_manager: UIManager,
        universe_simulator: UniverseSimulator,
    ) -> list[Post]:
        scene = self.reel.get(scene_no, None)
        if scene == None:
            return []

        return scene(ui_manager, universe_simulator)
