from atelier import Portrayer
from pygame import Surface

from paradox.domain import IntroPalette

root_portrayer = Portrayer()


@root_portrayer.occupy()
def render_intro_scene(palette: IntroPalette, render_screen: Surface, special_flags: int = 0) -> None:
    render_screen.fill((100, 100, 100, 255))
