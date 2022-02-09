from enum import Enum, unique


@unique
class SceneNo(int, Enum):
    INTRO: int = 0
    INGAME: int = 1
