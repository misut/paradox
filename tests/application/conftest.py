from loguru import logger
from pytest import fixture

from paradox.application import UIManager


@fixture(name="ui_manager", scope="package")
def create_ui_manager() -> UIManager:
    logger.remove()
    yield UIManager(pos=(0, 0), size=(100, 100))
