from loguru import logger
from pydantic import BaseModel, Field
from pygame import Surface

from paradox.domain.posts import Post
from paradox.domain.uis import UI


class UIManager(BaseModel):
    root_ui: UI

    hovering_ui: UI = Field(default=None)

    def __init__(self, size: tuple[int, int]) -> None:
        super().__init__(root_ui=UI(size=size))
        self.hovering_ui = self.root_ui

    def allocate(self, ui: UI) -> None:
        self.root_ui.allocate(ui)

    def click(self, pos: tuple[int, int]) -> Post | None:
        clicked_ui = self.root_ui.at(pos)
        if clicked_ui is None:
            return None
        
        logger.info(f"Clicked UI: {clicked_ui}")
        return clicked_ui.click()

    def hover(self, pos: tuple[int, int]) -> Post | None:
        hovering_ui = self.root_ui.at(pos)
        if hovering_ui is None:
            return None
        if hovering_ui.id == self.hovering_ui.id:
            return None
        
        self.hovering_ui = hovering_ui
        logger.info(f"Hovering over UI: {self.hovering_ui}")
        return self.hovering_ui.hover()

    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        self.root_ui.render(render_screen, special_flags)
