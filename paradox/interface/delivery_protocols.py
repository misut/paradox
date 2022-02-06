import sys

import pygame
from dependency_injector.wiring import Provide, inject
from loguru import logger
from postoffice import Postman
from pygame import Surface
from pygame.event import Event

from paradox.application import Gamepad, UIManager, UniverseSimulator
from paradox.domain import (
    KeyDownPost,
    KeyUpPost,
    MouseButtonDownPost,
    MouseButtonUpPost,
    MouseMotionPost,
    Post,
    QuitPost,
    TickPost,
)
from paradox.interface.container import Container

chief_postman = Postman()


def screen_pos_to_render_pos(
    pos: tuple[int, int],
    render_size: tuple[int, int],
    screen_size: tuple[int, int],
) -> tuple[int, int]:
    return (
        int(pos[0] * (render_size[0] / screen_size[0])),
        int(pos[1] * (render_size[1] / screen_size[1])),
    )


def propagate_event_to_post(
    event: Event, render_size: tuple[int, int], screen_size: tuple[int, int]
) -> Post | None:
    match event.type:
        case pygame.KEYDOWN:
            post = KeyDownPost(code=event.scancode)
        case pygame.KEYUP:
            post = KeyUpPost(code=event.scancode)
        case pygame.MOUSEBUTTONDOWN:
            pos = screen_pos_to_render_pos(event.pos, render_size, screen_size)
            post = MouseButtonDownPost(pos=pos, button=event.button, touch=event.touch)
        case pygame.MOUSEBUTTONUP:
            pos = screen_pos_to_render_pos(event.pos, render_size, screen_size)
            post = MouseButtonUpPost(pos=pos, button=event.button, touch=event.touch)
        case pygame.MOUSEMOTION:
            pos = screen_pos_to_render_pos(event.pos, render_size, screen_size)
            post = MouseMotionPost(
                pos=pos, rel=event.rel, buttons=event.buttons, touch=event.touch
            )
        case pygame.QUIT:
            post = QuitPost()
        case _:
            return None

    return post


@chief_postman.subscribe()
def deliver_quit_post(post: QuitPost) -> None:
    pygame.quit()
    sys.exit()


@chief_postman.subscribe()
@inject
def deliver_key_down_post(
    post: KeyDownPost,
    universe_simulator: UniverseSimulator = Provide[Container.universe_simulator],
) -> None:
    logger.debug(f"{post.code} is pressed")


@chief_postman.subscribe()
def deliver_key_up_post(post: KeyUpPost) -> None:
    logger.debug(f"{post.code} is released")


@chief_postman.subscribe()
@inject
def deliver_mouse_button_down_post(
    post: MouseButtonDownPost,
    ui_manager: UIManager = Provide[Container.ui_manager],
) -> list[Post]:
    logger.debug(f"{post.button} is pressed at {post.pos} {post.touch}")
    return ui_manager.click(post.pos)


@chief_postman.subscribe()
def deliver_mouse_button_up_post(post: MouseButtonUpPost) -> None:
    logger.debug(f"{post.button} is released at {post.pos} {post.touch}")


@chief_postman.subscribe()
@inject
def deliver_mouse_motion_post(
    post: MouseMotionPost,
    ui_manager: UIManager = Provide[Container.ui_manager],
) -> None:
    logger.debug(f"Mouse moved to {post.pos}. {post.rel} {post.buttons} {post.touch}")
    ui_manager.hover(post.pos)


@chief_postman.subscribe()
@inject
def deliver_tick_post(
    post: TickPost,
    render_screen: Surface = Provide[Container.render_screen],
    gamepad: Gamepad = Provide[Container.gamepad],
    ui_manager: UIManager = Provide[Container.ui_manager],
    universe_simulator: UniverseSimulator = Provide[Container.universe_simulator],
) -> None:
    logger.debug(f"{post}")

    gamepad.poll(post.ticks)
    universe_simulator.update(post.ticks)
    ui_manager.update(post.ticks)

    fps_count = ui_manager.get_uis_by_name("fps_count")[0]
    fps_count.text = str(int(post.fps))

    universe_simulator.render(render_screen, post.special_flags)
    ui_manager.render(render_screen, post.special_flags)
