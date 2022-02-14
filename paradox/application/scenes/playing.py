from paradox.application.film_director import FilmDirector
from paradox.application.ui_manager import UIManager
from paradox.application.universe_simulator import UniverseSimulator
from paradox.domain import Apparition, ApparitionTag, Post, SceneNo, SpriteTag

playing_director = FilmDirector()


@playing_director.take(SceneNo.PLAYING)
def playing_scene(
    ui_manager: UIManager, universe_simulator: UniverseSimulator
) -> list[Post]:
    ui_manager.clear()
    universe_simulator.resume()

    test_apparition = Apparition(
        name="test_apparition",
        coo=(-0.5, -0.5),
        dim=(1.0, 1.0),
        sprite=SpriteTag.APPARITION_TEST,
        tag=ApparitionTag.PLAYER,
    )
    # universe_simulator.place(test_apparition)
    # universe_simulator.universe.camera.attached = test_apparition
