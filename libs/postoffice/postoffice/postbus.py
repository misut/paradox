from abc import ABC, abstractmethod
from multiprocessing import Queue
from typing import Generator

from postoffice import Post


class Postbus(ABC):
    @abstractmethod
    def empty(self) -> bool:
        ...
    
    @abstractmethod
    def load(self, post: Post) -> None:
        ...

    @abstractmethod
    def unload(self) -> Generator[Post, None, None]:
        ...


class InMemoryPostbus(Postbus):
    trunk: Queue

    def __init__(self) -> None:
        self.trunk = Queue()

    def empty(self) -> bool:
        return self.trunk.empty()

    def load(self, post: Post) -> None:
        self.trunk.put(post)

    def unload(self) -> Generator[Post, None, None]:
        while not self.empty():
            yield self.trunk.get()
