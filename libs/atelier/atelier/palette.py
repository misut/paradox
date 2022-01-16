from abc import ABC

from pydantic import BaseModel


class Palette(ABC, BaseModel):
    ...
