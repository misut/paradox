from loguru import logger
from pydantic import BaseModel
from pygame import Surface

from paradox.domain import UI, UUID, Post


class UIManager(BaseModel):
    root_ui: UI

    clicking_ui: UI | None
    hovering_ui: UI | None

    def __init__(self, pos: tuple[int, int], size: tuple[int, int]) -> None:
        super().__init__(root_ui=UI(pos=pos, size=size))

    def allocate(self, ui: UI) -> None:
        self.root_ui.allocate(ui)

    def clear(self) -> None:
        self.root_ui.clear()
        self.hovering_ui = None

    def get_ui_by_id(self, id: UUID) -> UI | None:
        return self.root_ui.get_ui_by_id(id)

    def get_uis_by_name(self, name: str) -> list[UI]:
        return self.root_ui.get_uis_by_name(name)

    def click_on(self, pos: tuple[int, int]) -> list[Post]:
        clicked_on_ui = self.root_ui.at(pos)
        if clicked_on_ui == None:
            return []

        self.clicking_ui = clicked_on_ui
        logger.info(f"Clicked on UI: {clicked_on_ui.name}({clicked_on_ui.id})")
        return clicked_on_ui.click_on()

    def click_off(self, pos: tuple[int, int]) -> list[Post]:
        clicked_off_ui = self.root_ui.at(pos)
        if clicked_off_ui == None:
            self.clicking_ui = None
            return []
        if self.clicking_ui != clicked_off_ui:
            self.clicking_ui = None
            return []

        self.clicking_ui = None
        logger.info(f"Clicked off UI: {clicked_off_ui.name}({clicked_off_ui.id})")
        return clicked_off_ui.click_off()

    def hover(self, pos: tuple[int, int]) -> list[Post]:
        hovering_ui = self.root_ui.at(pos)
        if self.hovering_ui == hovering_ui:
            return []

        posts = []
        if self.hovering_ui:
            posts.extend(self.hovering_ui.hover_off())
            logger.info(f"Hovering out of UI: {hovering_ui.name}({hovering_ui.id})")

        self.hovering_ui = hovering_ui
        if self.hovering_ui:
            posts.extend(self.hovering_ui.hover_on())
            logger.info(f"Hovering over UI: {hovering_ui.name}({hovering_ui.id})")

        return posts

    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        self.root_ui.render(render_screen, special_flags)

    def update(self, ticks: int) -> None:
        self.root_ui.update(ticks)
