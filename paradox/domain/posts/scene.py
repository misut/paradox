from enum import Enum, unique

from paradox.domain.posts.base import Post


@unique
class SceneNo(int, Enum):
    INTRO: int = 0
    INGAME: int = 1
    SETTING: int = 2


class ShootScenePost(Post):
    scene_no: SceneNo
