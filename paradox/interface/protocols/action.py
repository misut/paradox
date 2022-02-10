from loguru import logger
from postoffice import Postman

from paradox.domain import ActionPost, Post

action_postman = Postman()


@action_postman.subscribe()
def deliver_action_post(post: ActionPost) -> None:
    logger.info(post)
