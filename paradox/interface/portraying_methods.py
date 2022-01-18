from atelier import Portrayer
from dependency_injector.wiring import Provide, inject
from pygame import Surface

from paradox.application import UIManager
from paradox.domain import IntroPalette
from paradox.interface.container import Container

root_portrayer = Portrayer()


@root_portrayer.occupy()
@inject
def render_intro_scene(
    palette: IntroPalette,
    ui_manager: UIManager = Provide[Container.ui_manager],
    render_screen: Surface = Provide[Container.render_screen],
) -> None:
    render_screen.fill((100, 100, 100, 255))

    ui_manager.render(render_screen, palette.special_flags)
