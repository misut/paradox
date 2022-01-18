from typing import Any

from atelier.portrayer import Portrayer

from pygame import Surface


class Atelier:
    root_portrayer: Portrayer

    def __init__(self) -> None:
        self.root_portrayer = Portrayer()

    def recruit(self, portrayer: Portrayer) -> None:
        self.root_portrayer.invite(portrayer)

    def portray(self, palette: Any) -> None:
        self.root_portrayer.portray(palette)
