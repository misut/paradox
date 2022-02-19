import sys

import pygame
from dependency_injector.wiring import Provide, inject
from loguru import logger
from postoffice import Postman
from pygame import Surface

from paradox.application import UIManager, UniverseSimulator
from paradox.domain import QuitPost, TickPost
from paradox.interface import Container

base_postman = Postman()


@base_postman.subscribe()
def deliver_quit_post(post: QuitPost) -> None:
    pygame.quit()
    sys.exit()


@base_postman.subscribe()
@inject
def deliver_tick_post(
    post: TickPost,
    render_screen: Surface = Provide[Container.render_screen],
    ui_manager: UIManager = Provide[Container.ui_manager],
    universe_simulator: UniverseSimulator = Provide[Container.universe_simulator],
) -> None:
    logger.debug(f"{post}")
    
    universe_simulator.act(post.actions)

    universe_simulator.update(post.ticks)
    ui_manager.update(post.ticks, fps=post.fps)

    universe_simulator.render(render_screen, post.special_flags)
    ui_manager.render(render_screen, post.special_flags)
