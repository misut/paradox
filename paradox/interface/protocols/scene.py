from dependency_injector.wiring import Provide, inject
from loguru import logger
from postoffice import Postman

from paradox.application import FilmDirector, UIManager, UniverseSimulator
from paradox.domain import Post, ShootScenePost
from paradox.interface import Container

scene_postman = Postman()


@scene_postman.subscribe()
@inject
def deliver_shoot_scene_post(
    post: ShootScenePost,
    film_director: FilmDirector = Provide[Container.film_director],
    ui_manager: UIManager = Provide[Container.ui_manager],
    universe_simulator: UniverseSimulator = Provide[Container.universe_simulator]
) -> list[Post]:
    logger.info(f"Shoot scene: {post.scene_no.name} #{post.scene_no}")
    return film_director.shoot(post.scene_no, ui_manager, universe_simulator)
