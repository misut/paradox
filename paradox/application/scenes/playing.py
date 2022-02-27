from paradox.application.film_director import FilmDirector
from paradox.application.ui_manager import UIManager
from paradox.application.universe_simulator import UniverseSimulator
from paradox.domain import (
    ApparitionStatus,
    ApparitionTag,
    Character,
    Direction,
    LayoutUI,
    Post,
    SceneNo,
    SpriteTag,
    TextUI,
    sprite_assets,
)

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
        size=(20, 10),
        cycletime=100,
        background_color=(0, 0, 0, 0),
        font_size=11,
        debug=True,
    )

    @fps_count.on_cycle()
    def cycle_fps_count(self_ui: TextUI) -> None:
        self_ui.text = str(int(self_ui.debug_info["fps"]))

    playing_ui.allocate(fps_count)

    ui_manager.allocate(playing_ui)

    test_sprite = sprite_assets.copy(SpriteTag.APPARITION_SLIME)

    test_apparition = Character(
        name="test_character",
        tag=ApparitionTag.PLAYER,
        coo=(0.5, 0.5),
        roo=(0.5, 0.5),
        dim=(0.3, 1.0),
        sprites={
            status: {
                Direction.NORTH: test_sprite,
                Direction.NORTHEAST: test_sprite,
                Direction.NORTHWEST: test_sprite,
                Direction.EAST: test_sprite,
                Direction.WEST: test_sprite,
                Direction.SOUTH: test_sprite,
                Direction.SOUTHEAST: test_sprite,
                Direction.SOUTHWEST: test_sprite,
            }
            for status in ApparitionStatus
        },
        velocity_limit=5.0,
        jump_limit=2,
    )
    universe_simulator.place(test_apparition)
    universe_simulator.universe.camera.attached = test_apparition
