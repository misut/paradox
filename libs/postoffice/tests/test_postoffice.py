from postoffice import Postbus, Postman, Postoffice
from pydantic import BaseModel


class RequestPost(BaseModel):
    ...


class ResultPost(BaseModel):
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
