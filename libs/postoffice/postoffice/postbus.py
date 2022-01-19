from abc import ABC, abstractmethod
from collections.abc import Generator
from multiprocessing import Queue
from typing import Any


class Postbus(ABC):
    @abstractmethod
    def empty(self) -> bool:
        ...

    @abstractmethod
    def load(self, post: Any) -> None:
        ...

    @abstractmethod
    def unload(self) -> Generator[Any, None, None]:
        ...


class InMemoryPostbus(Postbus):
    trunk: Queue

    def __init__(self) -> None:
        self.trunk = Queue()

    def empty(self) -> bool:
        return self.trunk.empty()

    def load(self, post: Any) -> None:
        self.trunk.put(post)

    def unload(self) -> Generator[Any, None, None]:
        while not self.empty():
            yield self.trunk.get()
