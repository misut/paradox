import pytest

from postoffice import Post, Postbus, Postman, Postoffice


class RequestPost(Post):
    ...


class ResultPost(Post):
    ...


def test_request_and_transport(postbus: Postbus, postoffice: Postoffice) -> None:
    postman = Postman()

    @postman.subscribe()
    def test_protocol(post: RequestPost) -> ResultPost:
        return ResultPost()

    postoffice.hire(postman)
    postoffice.request(RequestPost())
    postoffice.transport(postbus)

    assert isinstance(postoffice.warehouse.get(), ResultPost)
