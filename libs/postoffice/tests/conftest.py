from pytest import fixture

from postoffice import InMemoryPostbus, Postbus, Postoffice


@fixture(name="postbus", scope="package")
def create_inmemory_postbus() -> Postbus:
    yield InMemoryPostbus()


@fixture(name="postoffice", scope="package")
def create_postoffice() -> Postoffice:
    yield Postoffice()
