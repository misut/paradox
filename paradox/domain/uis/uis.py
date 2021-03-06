from __future__ import annotations

from pydantic import Field
from pygame import Surface
from pygame.font import Font

from paradox.domain.uis.base import (
    UI,
    HorizontalAlignment,
    VerticalAlignment,
    fit_pos,
    fit_rect,
)
from paradox.domain.uis.font import FontFace, FontWeight, font_assets


class LayoutUI(UI):
    def can_allocate(self, ui: UI) -> bool:
        if not self.embracing(ui):
            return False
        return super().can_allocate(ui)


class TextUI(UI):
    background_color: tuple[int, int, int, int] = Field(default=(255, 255, 255, 255))

    text: str = Field(default="text")
    text_horizontal_alignment: HorizontalAlignment = Field(default="center")
    text_vertical_alignment: VerticalAlignment = Field(default="middle")

    font_color: tuple[int, int, int, int] = Field(default=(0, 0, 0, 255))
    font_face: FontFace = Field(default=FontFace.NotoSans)
    font_size: int = Field(default=40)
    font_weight: FontWeight = Field(default=FontWeight.REGULAR)

    @property
    def font(self) -> Font:
        return font_assets.get(self.font_face, self.font_size, self.font_weight)

    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        super().render(render_screen, special_flags)

        text_surface = self.font.render(self.text, True, self.font_color)
        text_size = text_surface.get_size()

        dest = fit_pos(
            text_size,
            self.pos,
            self.size,
            self.text_horizontal_alignment,
            self.text_vertical_alignment,
        )
        rect = fit_rect(
            text_size,
            self.pos,
            self.size,
            self.text_horizontal_alignment,
            self.text_vertical_alignment,
        )
        render_screen.blit(text_surface, dest, rect, special_flags)
