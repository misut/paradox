from __future__ import annotations

from collections.abc import Callable
from enum import Enum, unique
from typing import Any

import pygame
from pydantic import Field
from pygame import Rect, Surface

from paradox.domain.base import ID, Entity, Renderable, Updatable
from paradox.domain.errors import UIAllocateError
from paradox.domain.posts import Post

Actor = Callable[["UI"], list[Post]]


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
        0 if aligned_pos[1] >= parent_pos[1] else parent_pos[1] - aligned_pos[1],
        parent_size[0],
        parent_size[1],
    )

    return fit_rect


@unique
class HorizontalAlignment(str, Enum):
    CENTER: str = "center"
    LEFT: str = "left"
    RIGHT: str = "right"


@unique
class VerticalAlignment(str, Enum):
    BOTTOM: str = "bottom"
    MIDDLE: str = "middle"
    TOP: str = "top"


class UI(Entity, Renderable, Updatable):
    childs: list[UI] = Field(default=[])
    parent: UI | None
    priority: int = Field(default=0)

    background_color: tuple[int, int, int, int] = Field(default=(0, 0, 0, 0))
    background_image: Surface | None

    # TODO: Not used
    horizontal_alignment: HorizontalAlignment = Field(default=HorizontalAlignment.LEFT)
    # TODO: Not used
    vertical_alignment: VerticalAlignment = Field(default=VerticalAlignment.TOP)

    click_on_action: Actor = Field(default=lambda _: [])
    click_off_action: Actor = Field(default=lambda _: [])
    cycle_action: Actor = Field(default=lambda _: [])
    hover_on_action: Actor = Field(default=lambda _: [])
    hover_off_action: Actor = Field(default=lambda _: [])

    debug: bool = Field(default=False)
    debug_info: dict[str, Any] = Field(default={})

    class Config:
        arbitrary_types_allowed = True

    def __eq__(self, other: UI) -> bool:
        if not isinstance(other, UI):
            return False
        return self.id == other.id

    def __lt__(self, other: UI) -> bool:
        return self.priority < other.priority

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
            raise UIAllocateError(
                f"Parent{self.size} at {self.pos}, Child{ui.size} at {ui.pos}"
            )

        overlapping_ui = self.at(ui.pos)
        ui.priority = overlapping_ui.priority

        ui.parent = self
        self.childs.insert(0, ui)
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

    def clear(self) -> None:
        for child in self.childs:
            child.clear()
        self.childs.clear()

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

    def get_ui_by_id(self, id: ID) -> UI | None:
        if self.id == id:
            return self

        for child in self.childs:
            ui = child.get_ui_by_id(id)
            if ui.id == id:
                return ui

        return None

    def get_uis_by_name(self, name: str) -> list[UI]:
        uis = []
        if self.name == name:
            uis.append(self)

        for child in self.childs:
            uis.extend(child.get_uis_by_name(name))

        return uis

    def on_click(self) -> Callable[[Actor], Actor]:
        def decorator(listener: Actor) -> Actor:
            self.click_on_action = listener
            return listener

        return decorator

    def off_click(self) -> Callable[[Actor], Actor]:
        def decorator(listener: Actor) -> Actor:
            self.click_off_action = listener
            return listener

        return decorator

    def on_cycle(self, debug: bool = False) -> Callable[[Actor], Actor]:
        def decorator(listener: Actor) -> Actor:
            self.cycle_action = listener
            return listener

        return decorator

    def on_hover(self) -> Callable[[Actor], Actor]:
        def decorator(listener: Actor) -> Actor:
            self.hover_on_action = listener
            return listener

        return decorator

    def off_hover(self) -> Callable[[Actor], Actor]:
        def decorator(listener: Actor) -> Actor:
            self.hover_off_action = listener
            return listener

        return decorator

    def click_on(self) -> list[Post]:
        return self.click_on_action(self)

    def click_off(self) -> list[Post]:
        return self.click_off_action(self)

    def cycle(self) -> None:
        self.cycle_action(self)

    def hover_on(self) -> list[Post]:
        return self.hover_on_action(self)

    def hover_off(self) -> list[Post]:
        return self.hover_off_action(self)

    def render(self, render_screen: Surface, special_flags: int = 0) -> None:
        render_screen.blit(
            source=self.background, dest=self.pos, special_flags=special_flags
        )

        for child in self.childs:
            child.render(render_screen, special_flags)

    def update(self, ticks: int, **debug_info) -> None:
        for child in self.childs:
            child.update(ticks, **debug_info)
        if self.debug:
            self.debug_info.update(debug_info)
        super().update(ticks)
        
