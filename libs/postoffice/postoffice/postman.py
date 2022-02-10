from __future__ import annotations

from collections.abc import Callable
from typing import Any, Concatenate, ParamSpec

from postoffice.errors import PostNotSubscribedError
from pydantic import BaseModel, Field

Params = ParamSpec("Params")
DeliveryProtocol = Callable[Concatenate[Any, Params], list | None]


class Postman(BaseModel):
    mapping: dict[Any, DeliveryProtocol] = Field(default={})

    def deliver(self, post: Any) -> list | None:
        post_type = type(post)
        if post_type not in self.mapping:
            raise PostNotSubscribedError(
                f"Not subscribed type of a post: {post_type.__name__}"
            )

        delivery_protocol = self.mapping[post_type]
        return delivery_protocol(post)

    def invite(self, *postmen: Postman) -> None:
        for postman in postmen:
            self.mapping.update(postman.mapping)

    def subscribe(self) -> Callable[[DeliveryProtocol], DeliveryProtocol]:
        def decorator(delivery_protocol: DeliveryProtocol) -> DeliveryProtocol:
            params = list(delivery_protocol.__annotations__)
            post_type = delivery_protocol.__annotations__[params[0]]
            self.mapping[post_type] = delivery_protocol
            return delivery_protocol

        return decorator
