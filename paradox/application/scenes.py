from enum import Enum, unique

from loguru import logger
from pydantic import BaseModel

from paradox.domain import LayoutUI, Post, QuitPost, TextUI, Universe


@unique
class SceneName(str, Enum):
    INTRO: str = "intro"
    PLAYING: str = "playing"


class Scene(BaseModel):
    layout: LayoutUI
    universe: Universe | None

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], universe: Universe | None = None) -> None:
        super().__init__(layout=LayoutUI(pos=pos, size=size, universe=universe))
        self.initialize()

    def initialize_debug_ui(self) -> None:
        fps_count = TextUI(
            name="fps_count",
            pos=(0, 0),
            size=(30, 20),
            background_color=(0, 0, 0, 0),
            font_size=23,
        )
        self.layout.allocate(fps_count)

    def initialize(self) -> None:
        raise NotImplementedError


class IntroScene(Scene):
    def initialize(self) -> None:
        self.initialize_debug_ui()

        quit_button = TextUI(pos=(100, 100), size=(200, 50), text="Quit")
        @quit_button.on_click()
        def click_sample_text(self_ui: TextUI) -> list[Post]:
            logger.info(f"Pressed {self_ui.text}")
            return [QuitPost()]
        self.layout.allocate(quit_button)


class PlayingScene(Scene):
    def initialize(self) -> None:
        ...
