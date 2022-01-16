import sys

from loguru import logger
from postoffice import Postman
import pygame

from paradox.domain import (
    KeyDownPost,
    KeyUpPost,
    MouseButtonDownPost,
    MouseButtonUpPost,
    MouseMotionPost,
    QuitPost,
)

chief_postman = Postman()


@chief_postman.subscribe()
def deliver_quit_post(post: QuitPost) -> None:
    pygame.quit()
    sys.exit()


@chief_postman.subscribe()
def deliver_key_down_post(post: KeyDownPost) -> None:
    logger.debug(f"{post.code} is pressed")


@chief_postman.subscribe()
def deliver_key_up_post(post: KeyUpPost) -> None:
    logger.debug(f"{post.code} is released")


@chief_postman.subscribe()
def deliver_mouse_button_down_post(post: MouseButtonDownPost) -> None:
    logger.debug(f"{post.button} is pressed at {post.pos} {post.touch}")


@chief_postman.subscribe()
def deliver_mouse_button_up_post(post: MouseButtonUpPost) -> None:
    logger.debug(f"{post.button} is released at {post.pos} {post.touch}")


@chief_postman.subscribe()
def deliver_mouse_motion_post(post: MouseMotionPost) -> None:
    logger.debug(f"Mouse moved to {post.pos}. {post.rel} {post.buttons} {post.touch}")
