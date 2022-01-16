from atelier.palette import Palette
from atelier.portrayer import Portrayer

from pygame import Surface


class Atelier:
    root_portrayer: Portrayer

    def __init__(self) -> None:
        self.root_portrayer = Portrayer()

    def recruit(self, portrayer: Portrayer) -> None:
        self.root_portrayer.invite(portrayer)

    def portray(self, palette: Palette, portrait: Surface, special_flags: int = 0) -> None:
        self.root_portrayer.portray(palette, portrait, special_flags)
