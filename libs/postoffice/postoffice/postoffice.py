from multiprocessing import Queue

from postoffice.post import Post
from postoffice.postbus import Postbus
from postoffice.postman import Postman


class Postoffice:
    chief_postman: Postman
    warehouse: Queue

    def __init__(self) -> None:
        self.chief_postman = Postman()
        self.warehouse = Queue()

    def hire(self, postman: Postman) -> None:
        self.chief_postman.invite(postman)

    def deliver(self, post: Post) -> Post | None:
        return self.chief_postman.deliver(post)

    def request(self, post: Post) -> None:
        self.warehouse.put(post)

    def transport(self, postbus: Postbus) -> None:
        while not self.warehouse.empty():
            postbus.load(self.warehouse.get())

        for post in postbus.unload():
            request_post = self.deliver(post)
            if request_post is None:
                continue

            self.request(request_post)
