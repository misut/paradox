from loguru import logger

from paradox.application.film_director import FilmDirector
from paradox.application.ui_manager import UIManager
from paradox.application.universe_simulator import UniverseSimulator
from paradox.domain import LayoutUI, Post, SceneNo, ShootScenePost, TextUI

setting_director = FilmDirector()


@setting_director.take(SceneNo.SETTING)
def setting_scene(ui_manager: UIManager, universe_simulator: UniverseSimulator) -> list[Post]:
    ui_manager.clear()
    universe_simulator.pause()

    setting_ui = LayoutUI(pos=(0, 0), size=ui_manager.root_ui.size)

    apply_button = TextUI(
        name="apply_button",
        pos=(270, 160),
        size=(100, 40),
        background_color=(255, 255, 255, 0),
        font_size=31,
        text="Apply",
    )

    back_button = TextUI(
        name="back_button",
        pos=(270, 220),
        size=(100, 40),
        background_color=(255, 255, 255, 0),
        font_size=31,
        text="Back",
    )

    @apply_button.on_click()
    @back_button.on_click()
    def click_on_button(self_ui: TextUI) -> list[Post]:
        logger.info(f"Clicked on {self_ui.name}")
        self_ui.background_color = (255, 255, 255, 32)

    @apply_button.off_click()
    def click_off_apply_button(self_ui: TextUI) -> list[Post]:
        self_ui.background_color = (255, 255, 255, 0)

    @back_button.off_click()
    def click_off_back_button(self_ui: TextUI) -> list[Post]:
        self_ui.background_color = (255, 255, 255, 0)
        return [ShootScenePost(scene_no=SceneNo.INTRO)]

    @apply_button.on_hover()
    @back_button.on_hover()
    def hover_on_button(self_ui: TextUI) -> list[Post]:
        self_ui.font_color = (255, 255, 255, 255)
        return []

    @apply_button.off_hover()
    @back_button.off_hover()
    def hover_off_button(self_ui: TextUI) -> list[Post]:
        self_ui.font_color = (0, 0, 0, 255)
        return []

    setting_ui.allocate(apply_button)
    setting_ui.allocate(back_button)

    ui_manager.allocate(setting_ui)

    return []
