from typing import Generator

from postoffice import Postman, PostNotSubscribedError
from pydantic import BaseModel
from pytest import fixture, raises


class NotSubscribedPost(BaseModel):
    ...


class ThisPost(BaseModel):
    ...


class ThatPost(BaseModel):
    ...


@fixture(name="not_subscribed_post", scope="module")
def create_not_subscribed_post() -> Generator[NotSubscribedPost, None, None]:
    yield NotSubscribedPost()


def test_fresh_postman(not_subscribed_post: NotSubscribedPost) -> None:
    postman = Postman()

    with raises(PostNotSubscribedError):
        postman.deliver(not_subscribed_post)


def test_subscribe_and_deliver() -> None:
    senior_postman = Postman()

    @senior_postman.subscribe()
    def this_protocol(post: ThisPost) -> None:
        pass

    junior_postman = Postman()

    @junior_postman.subscribe()
    def that_protocol(post: ThatPost) -> None:
        pass

    senior_postman.invite(junior_postman)

    senior_postman.deliver(ThisPost())
    senior_postman.deliver(ThatPost())
