from dependency_injector.wiring import Provide, inject
from loguru import logger
from postoffice import Postman

from paradox.application import UIManager
from paradox.domain import EventType, MouseEventPost, MouseMotionPost, Post
from paradox.interface import Container

event_postman = Postman()


@event_postman.subscribe()
@inject
def deliver_mouse_event_post(
    post: MouseEventPost,
    ui_manager: UIManager = Provide[Container.ui_manager],
) -> list[Post]:
    if post.type == EventType.UP:
        logger.debug(f"{post.button} is released at {post.pos}")
        return ui_manager.click_off(post.pos)
    logger.debug(f"{post.button} is pressed at {post.pos}")
    return ui_manager.click_on(post.pos)


@event_postman.subscribe()
@inject
def deliver_mouse_motion_post(
    post: MouseMotionPost,
    ui_manager: UIManager = Provide[Container.ui_manager],
) -> None:
    logger.debug(f"Mouse moved to {post.pos}. {post.rel} {post.buttons}")
    ui_manager.hover(post.pos)
