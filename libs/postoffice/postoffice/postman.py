from __future__ import annotations

from collections.abc import Callable
from typing import Concatenate, ParamSpec

from pydantic import BaseModel, Field

from postoffice.errors import PostNotSubscribedError
from postoffice.post import Post


Params = ParamSpec("Params")
DeliveryProtocol = Callable[Concatenate[Post, Params], Post | None]


class Postman(BaseModel):
    mapping: dict[type[Post], DeliveryProtocol] = Field(default={})

    def deliver(self, post: Post) -> Post | None:
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
