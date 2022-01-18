from __future__ import annotations

from collections.abc import Callable
from typing import ParamSpec

from pydantic import Field
from pygame import Rect, Surface
import pygame

from paradox.domain.base import Entity
from paradox.domain.enums import HorizontalAlignment, VerticalAlignment
from paradox.domain.posts import Post

Params = ParamSpec("Params")
Actor = Callable[Params, Post | None]


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

    return(aligned_pos_x, aligned_pos_y)


def fit_pos(
    size: tuple[int, int],
    parent_pos: tuple[int, int],
    parent_size: tuple[int, int],
    horizontal_alignment: HorizontalAlignment,
    vertical_alignment: VerticalAlignment,
) -> tuple[int, int]:
    aligned_pos = align_pos(
        size,
        parent_pos,
        parent_size,
        horizontal_alignment,
        vertical_alignment,
    )

    fit_pos = (
        max(aligned_pos[0], parent_pos[0]),
        max(aligned_pos[1], parent_pos[1]),
    )

    return fit_pos


def fit_rect(
    size: tuple[int, int],
    parent_pos: tuple[int, int],
    parent_size: tuple[int, int],
    horizontal_alignment: HorizontalAlignment,
    vertical_alignment: VerticalAlignment,
) -> Rect:
    aligned_pos = align_pos(
        size,
        parent_pos,
        parent_size,
        horizontal_alignment,
        vertical_alignment,
    )

    fit_rect = Rect(
        0 if aligned_pos[0] >= parent_pos[0] else parent_pos[0] - aligned_pos[0],
        0 if aligned_pos[1] >= parent_pos[1]  else parent_pos[1] - aligned_pos[1],
        parent_size[0],
        parent_size[1],
    )

    return fit_rect


class UI(Entity):
    pos: tuple[int, int] = Field(default=(0, 0))
    size: tuple[int, int]

    childs: list[UI] = Field(default=[])
    parent: UI | None
    priority: int = Field(default=0)

    background_color: tuple[int, int, int, int] = Field(default=(0, 0, 0, 0))
    background_image: Surface | None

    horizontal_alignment: HorizontalAlignment = Field(default=HorizontalAlignment.LEFT)  # TODO: Not used
    vertical_alignment: VerticalAlignment = Field(default=VerticalAlignment.TOP)  # TODO: Not used

    click_action: Actor = Field(default=lambda: None)
    hover_action: Actor = Field(default=lambda: None)

    class Config:
        arbitrary_types_allowed = True

    def __lt__(self, other: UI) -> bool:
        return self.priority < other.priority

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
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self) -> int:
        return self.size[1]

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

        overlapping_uis = [child for child in self.childs if child.overlapping(ui)]
        if not overlapping_uis:
            ui.priority = self.priority
        else:
            ui.priority = max(oui.priority for oui in overlapping_uis)
        self.childs.append(ui)
        self.childs.sort(reverse=True)

    def at(self, pos: tuple[int, int]) -> UI | None:
        if not self.including(pos):
            return None

        for ui in self.childs:
            if ui.including(pos):
                return ui.at(pos)
        
        return self

    def can_allocate(self, ui: UI) -> bool:
        if ui in self.childs:
            return False
        
        return True

    def embracing(self, ui: UI) -> bool:
        if ui.left < self.left:
            return False
        if ui.right > self.right:
            return False
        if ui.top < self.top:
            return False
        if ui.bottom > self.bottom:
            return False
        return True

    def including(self, pos: tuple[int, int]) -> bool:
        if not self.left <= pos[0] <= self.right:
            return False
        if not self.top <= pos[1] <= self.bottom:
            return False
        return True

    def overlapping(self, ui: UI) -> bool:
        if self.including((ui.left, ui.top)):
            return True
        if self.including((ui.left, ui.bottom)):
            return True
        if self.including((ui.right, ui.bottom)):
            return True
        if self.including((ui.right, ui.top)):
            return True
        return False

    def on_click(self) -> Callable[[Actor], Actor]:
        def decorator(listener: Actor) -> Actor:
            self.click_action = listener
            return listener
        return decorator

    def on_hover(self) -> Callable[[Actor], Actor]:
        def decorator(listener: Actor) -> Actor:
            self.hover_action = listener
            return listener
        return decorator

    def click(self) -> Post | None:
        return self.click_action()

    def hover(self) -> Post | None:
        return self.hover_action()

    def update(self) -> None:
        ...

    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        render_screen.blit(source=self.background, dest=self.pos, special_flags=special_flags)

        for child in self.childs:
            child.render(render_screen, special_flags)
