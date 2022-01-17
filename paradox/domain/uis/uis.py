from __future__ import annotations

from collections.abc import Callable

from postoffice import Post
from pydantic import Field
from pygame import Surface
from pygame.font import Font, SysFont

from paradox.domain.enums import HorizontalAlignment, VerticalAlignment
from paradox.domain.uis.base import UI, align_pos

Listener = Callable[[], Post | None]


class LayoutUI(UI):
    def can_allocate(self, ui: UI) -> bool:
        if not self.embrace(ui):
            return False
        return super().can_allocate(ui)


class TextUI(UI):
    background_color: tuple[int, int, int, int] = Field(default=(255, 255, 255, 255))

    text: str = Field(default="text")
    text_horizontal_alignment: HorizontalAlignment = Field(default="center")
    text_vertical_alignment: VerticalAlignment = Field(default="middle")

    font_face: str = Field(default="")
    font_size: int = Field(default=40)
    bold: bool = Field(default=False)
    italic: bool = Field(default=False)

    @property
    def font(self) -> Font:
        return SysFont(self.font_face, self.font_size, self.bold, self.italic)

    def draw(self, render_screen: Surface) -> None:
        super().draw(render_screen)

        text_surface = self.font.render(self.text, False, (0, 0, 0, 255))
        text_size = text_surface.get_size()

        aligned_pos = align_pos(text_size, self.pos, self.size, self.text_horizontal_alignment, self.text_vertical_alignment)
        render_screen.blit(text_surface, aligned_pos)


class ButtonUI(TextUI):
    on_click_listener: Listener = Field(default=lambda: None)

    def on_click(self, listener: Listener) -> Listener:
        self.on_click_listener = listener
        return listener
