from postoffice import InMemoryPostbus, Postbus, Postoffice
from pytest import fixture


@fixture(name="postbus", scope="package")
def create_inmemory_postbus() -> Postbus:
    yield InMemoryPostbus()


@fixture(name="postoffice", scope="package")
def create_postoffice() -> Postoffice:
    yield Postoffice()
