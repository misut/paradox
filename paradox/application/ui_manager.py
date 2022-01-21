from loguru import logger
from pygame import Surface

from paradox.domain import Post, UI, UUID


class UIManager:
    root_ui: UI

    hovering_ui: UI | None

    def __init__(self, pos: tuple[int, int], size: tuple[int, int]) -> None:
        self.root_ui = UI(pos=pos, size=size)
        self.hovering_ui = None

    def allocate(self, ui: UI) -> None:
        self.root_ui.allocate(ui)

    def get_ui_by_id(self, id: UUID) -> UI | None:
        return self.root_ui.get_ui_by_id(id)

    def get_uis_by_name(self, name: str) -> list[UI]:
        return self.root_ui.get_uis_by_name(name)

    def click(self, pos: tuple[int, int]) -> list[Post] | None:
        clicked_ui = self.root_ui.at(pos)
        if clicked_ui is None:
            return None

        logger.info(f"Clicked UI: {clicked_ui}")
        return clicked_ui.click()

    def hover(self, pos: tuple[int, int]) -> list[Post] | None:
        hovering_ui = self.root_ui.at(pos)
        if hovering_ui == None:
            return None
        if hovering_ui == self.hovering_ui:
            return None

        self.hovering_ui = hovering_ui
        logger.info(f"Hovering over UI: {self.hovering_ui}")
        return self.hovering_ui.hover()

    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        self.root_ui.render(render_screen, special_flags)