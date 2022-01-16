from abc import ABC

from pydantic import BaseModel


class Post(ABC, BaseModel):
    class Config:
        allow_mutation = False
