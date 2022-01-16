from __future__ import annotations

from typing import Callable, Optional

from pydantic import BaseModel, Field

from postoffice.errors import PostNotSubscribedError
from postoffice.post import Post


DeliveryProtocol = Callable[[Post], Optional[Post]]


class Postman(BaseModel):
    mapping: dict[type[Post], DeliveryProtocol] = Field(default={})

    def deliver(self, post: Post) -> Optional[Post]:
        post_type = type(post)
        if post_type not in self.mapping:
            raise PostNotSubscribedError(f"Not subscribed type of a post: {post_type.__name__}")
        
        delivery_protocol = self.mapping[post_type]
        return delivery_protocol(post)

    def invite(self, postman: Postman) -> None:
        self.mapping.update(postman.mapping)

    def subscribe(self) -> Callable[[DeliveryProtocol], DeliveryProtocol]:
        def decorator(delivery_protocol: DeliveryProtocol) -> DeliveryProtocol:
            params = list(delivery_protocol.__annotations__)
            post_type = delivery_protocol.__annotations__[params[0]]
            self.mapping[post_type] = delivery_protocol
            return delivery_protocol
        return decorator
