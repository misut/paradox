from __future__ import annotations

from pydantic import Field
from pygame import Surface
import pygame

from paradox.domain.base import Entity
from paradox.domain.enums import HorizontalAlignment, VerticalAlignment


def align_pos(
    size: tuple[int, int],
    parent_pos: tuple[int, int],
    parent_size: tuple[int, int],
    horizontal_alignment: HorizontalAlignment,
    vertical_alignment: VerticalAlignment,
) -> tuple[int, int]:
    aligned_pos_x = parent_pos[0]
    match horizontal_alignment:
        case HorizontalAlignment.CENTER:
            aligned_pos_x += (parent_size[0] - size[0]) // 2
        case HorizontalAlignment.LEFT:
            aligned_pos_x += 0
        case HorizontalAlignment.RIGHT:
            aligned_pos_x += parent_size[0] - size[0]

    aligned_pos_y = parent_pos[1]
    match vertical_alignment:
        case VerticalAlignment.MIDDLE:
            aligned_pos_y += (parent_size[1] - size[1]) // 2
        case VerticalAlignment.TOP:
            aligned_pos_y += 0
        case VerticalAlignment.BOTTOM:
            aligned_pos_y += parent_size[1] - size[1]

    return (aligned_pos_x, aligned_pos_y)


class UI(Entity):
    pos: tuple[int, int] = Field(default=(0, 0))
    size: tuple[int, int]

    childs: list[UI] = Field(default=[])
    parent: UI | None

    background_color: tuple[int, int, int, int] = Field(default=(0, 0, 0, 0))
    background_image: Surface | None

    horizontal_alignment: HorizontalAlignment = Field(default=HorizontalAlignment.LEFT)  # TODO: Not used
    vertical_alignment: VerticalAlignment = Field(default=VerticalAlignment.TOP)  # TODO: Not used

    class Config:
        arbitrary_types_allowed = True

    @property
    def left(self) -> int:
        return self.pos[0]

    @property
    def right(self) -> int:
        return self.pos[0] + self.size[0] - 1

    @property
    def top(self) -> int:
        return self.pos[1]

    @property
    def bottom(self) -> int:
        return self.pos[1] + self.size[1] - 1

    @property
    def background(self) -> Surface:
        if self.background_image is None:
            background = Surface(self.size, pygame.SRCALPHA)
            background.fill(self.background_color)
        else:
            background = self.background_image
        return background
    
    def allocate(self, ui: UI) -> None:
        if not self.can_allocate(ui):
            raise Exception(f"Failed to allocate UI({ui.__str__()}).")

        self.childs.append(ui)

    def can_allocate(self, ui: UI) -> bool:
        if ui in self.childs:
            return False
        
        return True

    def embrace(self, ui: UI) -> bool:
        if ui.left < self.left:
            return False
        if ui.right > self.right:
            return False
        if ui.top < self.top:
            return False
        if ui.bottom > self.bottom:
            return False
        return True

    def inside(self, pos: tuple[int, int]) -> bool:
        if not self.left < pos[0] < self.right:
            return False
        if not self.top < pos[1] < self.bottom:
            return False
        return True

    def update(self) -> None:
        ...

    def draw(self, render_screen: Surface, special_flags: int = 0) -> None:
        render_screen.blit(source=self.background, dest=self.pos, special_flags=special_flags)

        for child in self.childs:
            child.draw(render_screen)
