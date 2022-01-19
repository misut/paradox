from postoffice import Postbus
from pydantic import BaseModel


class SequencePost(BaseModel):
    idx: int


def test_load_and_unload_post(postbus: Postbus) -> None:
    for idx in range(10):
        postbus.load(SequencePost(idx=idx))

    for idx, post in enumerate(postbus.unload()):
        assert post.idx == idx
