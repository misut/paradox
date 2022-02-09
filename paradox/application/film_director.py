from collections.abc import Callable

from pydantic import BaseModel

from paradox.application.ui_manager import UIManager
from paradox.application.universe_simulator import UniverseSimulator
from paradox.domain import Post

Scene = Callable[[UIManager, UniverseSimulator], list[Post]]


class FilmDirector(BaseModel):
    ...