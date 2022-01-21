from atelier import Portrayer
from dependency_injector.wiring import Provide, inject
from pygame import Surface

from paradox.application import UIManager, UniverseSimulator
from paradox.domain import IntroPalette
from paradox.interface.container import Container

root_portrayer = Portrayer()


@root_portrayer.occupy()
@inject
def render_intro_scene(
    palette: IntroPalette,
    ui_manager: UIManager = Provide[Container.ui_manager],
    universe_simulator: UniverseSimulator = Provide[Container.universe_simulator],
    render_screen: Surface = Provide[Container.render_screen],
) -> None:
    universe_simulator.render(render_screen, palette.special_flags)
    ui_manager.render(render_screen, palette.special_flags)
