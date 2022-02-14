from dependency_injector.wiring import Provide, inject
from loguru import logger
from postoffice import Postman

from paradox.application import UniverseSimulator
from paradox.domain import ActionPost
from paradox.interface.container import Container

action_postman = Postman()


@action_postman.subscribe()
@inject
def deliver_action_post(
    post: ActionPost,
    universe_simulator: UniverseSimulator = Provide[Container.universe_simulator],
) -> None:
    logger.info(post)
    universe_simulator.act(post.infos)
