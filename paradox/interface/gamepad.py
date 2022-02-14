import pygame
from loguru import logger
from pydantic import BaseModel, Field
from pygame.event import Event as PygameEvent

from paradox.domain.posts import (
    Action,
    ActionInfo,
    ActionPost,
    ActionType,
    EventType,
    MouseEventPost,
    MouseMotionPost,
    QuitPost,
)
from paradox.interface.settings import GamepadSettings, GraphicSettings


def screen_pos_to_render_pos(
    pos: tuple[int, int],
    render_size: tuple[int, int],
    screen_size: tuple[int, int],
) -> tuple[int, int]:
    return (
        int(pos[0] * (render_size[0] / screen_size[0])),
        int(pos[1] * (render_size[1] / screen_size[1])),
    )


class Gamepad(BaseModel):
    gamepad_settings: GamepadSettings
    graphic_settings: GraphicSettings

    mapping: dict[Action, int] = Field(default={})
    scanning: dict[Action, int] = Field(default={})

    def __init__(
        self, gamepad_settings: GamepadSettings, graphic_settings: GraphicSettings
    ) -> None:
        super().__init__(
            gamepad_settings=gamepad_settings, graphic_settings=graphic_settings
        )

        for action_str, code in gamepad_settings:
            action = Action[action_str]
            self.mapping[action] = code
            self.scanning[action] = 0

    def fit_screen_pos_into_render_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        return (
            int(
                pos[0]
                * (
                    self.graphic_settings.RENDER_SIZE[0]
                    / self.graphic_settings.SCREEN_SIZE[0]
                )
            ),
            int(
                pos[1]
                * (
                    self.graphic_settings.RENDER_SIZE[1]
                    / self.graphic_settings.SCREEN_SIZE[1]
                )
            ),
        )

    def _propagate(self, event: PygameEvent) -> ActionPost | None:
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                post = MouseEventPost(
                    type=EventType.DOWN,
                    pos=self.fit_screen_pos_into_render_pos(event.pos),
                    button=event.button,
                )
            case pygame.MOUSEBUTTONUP:
                post = MouseEventPost(
                    type=EventType.UP,
                    pos=self.fit_screen_pos_into_render_pos(event.pos),
                    button=event.button,
                )
            case pygame.MOUSEMOTION:
                post = MouseMotionPost(
                    pos=self.fit_screen_pos_into_render_pos(event.pos),
                    rel=self.fit_screen_pos_into_render_pos(event.rel),
                    buttons=event.buttons,
                )
            case pygame.QUIT:
                post = QuitPost()
            case _:
                return None

        return post

    def propagate(self) -> list[ActionPost]:
        event_posts = []

        for event in pygame.event.get():
            event_post = self._propagate(event)
            if event_post == None:
                continue

            event_posts.append(event_post)

        return event_posts

    def poll(self, ticks: int) -> list[ActionPost]:
        action_infos = {}

        scancodes = list(pygame.key.get_pressed())
        for action, code in self.mapping.items():
            pressed = scancodes[code]
            duration = self.scanning[action]
            if not pressed and duration == 0:
                continue
            self.scanning[action] += ticks
            if pressed and duration == 0:
                action_info = ActionInfo(
                    action=action,
                    type=ActionType.PRESSED,
                    duration=self.scanning[action],
                )
                action_infos[action] = action_info
                continue

            if pressed and duration > 0:
                action_info = ActionInfo(
                    action=action,
                    type=ActionType.PRESSING,
                    duration=self.scanning[action],
                )
                action_infos[action] = action_info
                continue

            action_info = ActionInfo(
                action=action,
                type=ActionType.RELEASED,
                duration=self.scanning[action],
            )
            action_infos[action] = action_info
            self.scanning[action] = 0

        if not action_infos:
            return [ActionPost(infos={})]
        return [ActionPost(infos=action_infos)]

    def update(self, ticks: int) -> list[ActionPost]:
        return self.propagate() + self.poll(ticks)
