from pydantic import BaseModel, Field

from paradox.application.gamepad import Gamepad
from paradox.application.scenes import Scene, SceneName
from paradox.application.ui_manager import UIManager
from paradox.application.universe_simulator import UniverseSimulator


class FilmMaker(BaseModel):
    gamepad: Gamepad
    ui_manager: UIManager
    universe_simulator: UniverseSimulator

    scenes: list[Scene] = Field(default=[])
    scene_name: SceneName = Field(default=SceneName.INTRO)

    def take(self) -> None:
        ...
