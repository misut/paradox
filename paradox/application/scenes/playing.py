from paradox.application.film_director import FilmDirector
from paradox.application.ui_manager import UIManager
from paradox.application.universe_simulator import UniverseSimulator
from paradox.domain import Apparition, ApparitionTag, LayoutUI, Post, SceneNo, SpriteTag, TextUI

playing_director = FilmDirector()


@playing_director.take(SceneNo.PLAYING)
def playing_scene(
    ui_manager: UIManager, universe_simulator: UniverseSimulator
) -> list[Post]:
    ui_manager.clear()
    universe_simulator.resume()

    playing_ui = LayoutUI(pos=(0, 0), size=ui_manager.root_ui.size)

    fps_count = TextUI(
        name="fps_count",
        pos=(0, 0),
        size=(30, 20),
        cycletime=100,
        background_color=(0, 0, 0, 0),
        font_size=23,
        debug=True,
    )

    @fps_count.on_cycle()
    def cycle_fps_count(self_ui: TextUI) -> None:
        self_ui.text = str(int(self_ui.debug_info["fps"]))

    playing_ui.allocate(fps_count)

    ui_manager.allocate(playing_ui)

    test_apparition = Apparition(
        name="test_apparition",
        coo=(0.5, 0.5),
        roo=(0.5, 0.5),
        dim=(0.3, 1.0),
        sprite=SpriteTag.APPARITION_TEST,
        tag=ApparitionTag.PLAYER,
        velocity_limit=5.0,
        jump_count_limit=2,
    )
    universe_simulator.place(test_apparition)
    universe_simulator.universe.camera.attached = test_apparition
