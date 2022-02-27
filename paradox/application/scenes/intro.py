from loguru import logger

from paradox.application.film_director import FilmDirector
from paradox.application.ui_manager import UIManager
from paradox.application.universe_simulator import UniverseSimulator
from paradox.domain import FontWeight, LayoutUI, Post, QuitPost, SceneNo, ShootScenePost, TextUI

intro_director = FilmDirector()


@intro_director.take(SceneNo.INTRO)
def intro_scene(
    ui_manager: UIManager, universe_simulator: UniverseSimulator
) -> list[Post]:
    ui_manager.clear()
    universe_simulator.pause()

    intro_ui = LayoutUI(pos=(0, 0), size=ui_manager.root_ui.size)

    start_button = TextUI(
        name="start_button",
        pos=(270, 160),
        size=(100, 40),
        background_color=(255, 255, 255, 0),
        font_size=23,
        font_weight=FontWeight.MEDIUM,
        text="Start",
    )

    setting_button = TextUI(
        name="setting_button",
        pos=(270, 220),
        size=(100, 40),
        background_color=(255, 255, 255, 0),
        font_size=23,
        font_weight=FontWeight.MEDIUM,
        text="Setting",
    )

    quit_button = TextUI(
        name="quit_button",
        pos=(270, 280),
        size=(100, 40),
        background_color=(255, 255, 255, 0),
        font_size=23,
        font_weight=FontWeight.MEDIUM,
        text="Quit",
    )

    @start_button.on_click()
    @setting_button.on_click()
    @quit_button.on_click()
    def click_on_button(self_ui: TextUI) -> list[Post]:
        logger.info(f"Clicked on {self_ui.name}")
        self_ui.background_color = (255, 255, 255, 32)

    @start_button.off_click()
    def click_off_start_button(self_ui: TextUI) -> list[Post]:
        self_ui.background_color = (255, 255, 255, 0)
        return [ShootScenePost(scene_no=SceneNo.PLAYING)]

    @setting_button.off_click()
    def click_off_setting_button(self_ui: TextUI) -> list[Post]:
        self_ui.background_color = (255, 255, 255, 0)
        return [ShootScenePost(scene_no=SceneNo.SETTING)]

    @quit_button.off_click()
    def click_off_quit_button(self_ui: TextUI) -> list[Post]:
        logger.info(f"Clicked off {self_ui.name}")
        self_ui.background_color = (255, 255, 255, 0)
        return [QuitPost()]

    @start_button.on_hover()
    @setting_button.on_hover()
    @quit_button.on_hover()
    def hover_on_button(self_ui: TextUI) -> list[Post]:
        self_ui.font_color = (255, 255, 255, 255)
        return []

    @start_button.off_hover()
    @setting_button.off_hover()
    @quit_button.off_hover()
    def hover_off_button(self_ui: TextUI) -> list[Post]:
        self_ui.font_color = (0, 0, 0, 255)
        return []

    intro_ui.allocate(start_button)
    intro_ui.allocate(setting_button)
    intro_ui.allocate(quit_button)

    fps_count = TextUI(
        name="fps_count",
        pos=(0, 0),
        size=(20, 10),
        cycletime=100,
        background_color=(0, 0, 0, 0),
        font_size=11,
        debug=True,
    )

    @fps_count.on_cycle()
    def cycle_fps_count(self_ui: TextUI) -> None:
        self_ui.text = str(int(self_ui.debug_info["fps"]))

    intro_ui.allocate(fps_count)

    ui_manager.allocate(intro_ui)

    return []
