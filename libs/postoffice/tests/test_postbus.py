from pytest import fixture

from postoffice import InMemoryPostbus, Post, Postbus
    

class SequencePost(Post):
    idx: int


def test_load_and_unload_post(postbus: Postbus) -> None:
    for idx in range(10):
        postbus.load(SequencePost(idx=idx))
    
    for idx, post in enumerate(postbus.unload()):
        assert post.idx == idx
