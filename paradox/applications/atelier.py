from atelier import Atelier

from paradox.applications.rendering_methods import root_portrayer


class ParadoxAtelier(Atelier):
    def __init__(self) -> None:
        super().__init__()

        self.recruit(root_portrayer)
