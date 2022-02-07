import sys

import pygame
from dependency_injector.wiring import Provide, inject
from loguru import logger
from postoffice import Postman
from pygame import Surface

from paradox.application import UIManager, UniverseSimulator
from paradox.domain import (
    ActionPost,
    EventType,
    MouseButton,
    MouseEventPost,
    MouseMotionPost,
    Post,
    QuitPost,
    TickPost,
)
from paradox.interface.container import Container

chief_postman = Postman()


@chief_postman.subscribe()
def deliver_quit_post(post: QuitPost) -> None:
    pygame.quit()
    sys.exit()


@chief_postman.subscribe()
def deliver_action_post(
    post: ActionPost
) -> list[Post]:
    logger.info(post)


@chief_postman.subscribe()
@inject
def deliver_mouse_event_post(
    post: MouseEventPost,
    ui_manager: UIManager = Provide[Container.ui_manager],
) -> list[Post]:
    if post.type == EventType.UP:
        logger.debug(f"{post.button} is released at {post.pos}")
        return []
    return ui_manager.click(post.pos)


@chief_postman.subscribe()
@inject
def deliver_mouse_motion_post(
    post: MouseMotionPost,
    ui_manager: UIManager = Provide[Container.ui_manager],
) -> None:
    logger.debug(f"Mouse moved to {post.pos}. {post.rel} {post.buttons}")
    ui_manager.hover(post.pos)


@chief_postman.subscribe()
@inject
def deliver_tick_post(
    post: TickPost,
    render_screen: Surface = Provide[Container.render_screen],
    ui_manager: UIManager = Provide[Container.ui_manager],
    universe_simulator: UniverseSimulator = Provide[Container.universe_simulator],
) -> None:
    logger.debug(f"{post}")

    universe_simulator.update(post.ticks)
    ui_manager.update(post.ticks)

    fps_count = ui_manager.get_uis_by_name("fps_count")[0]
    fps_count.text = str(int(post.fps))

    universe_simulator.render(render_screen, post.special_flags)
    ui_manager.render(render_screen, post.special_flags)
