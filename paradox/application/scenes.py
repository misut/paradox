from loguru import logger

from paradox.application.film_director import FilmDirector
from paradox.application.ui_manager import UIManager
from paradox.application.universe_simulator import UniverseSimulator
from paradox.domain import LayoutUI, Post, QuitPost, SceneNo, TextUI

paradox_director = FilmDirector()


@paradox_director.take(SceneNo.INTRO)
def intro_scene(ui_manager: UIManager, universe_simulator: UniverseSimulator) -> Post:
    ui_manager.clear()

    intro_ui = LayoutUI(pos=(0, 0), size=ui_manager.root_ui.size)

    quit_button = TextUI(
        name="quit_button",
        pos=(0, 320),
        size=(100, 40),
        background_color=(255, 255, 255, 0),
        font_size=31,
        text="Quit",
    )

    @quit_button.off_click()
    def click_off_quit_button(self_ui: TextUI) -> list[Post]:
        logger.info(f"Clicked {self_ui.text}")
        return [QuitPost()]

    @quit_button.on_hover()
    def hover_on_quit_button(self_ui: TextUI) -> list[Post]:
        self_ui.background_color = (255, 255, 255, 32)
        return []

    @quit_button.off_hover()
    def hover_off_quit_button(self_ui: TextUI) -> list[Post]:
        self_ui.background_color = (255, 255, 255, 0)
        return []

    intro_ui.allocate(quit_button)

    ui_manager.allocate(intro_ui)
