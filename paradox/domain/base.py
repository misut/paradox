from uuid import UUID, uuid4

from pydantic import BaseModel, Field

generate_uuid = uuid4


class ValueObject(BaseModel):
    class Config:
        allow_mutation = False


class Entity(BaseModel):
    id: UUID = Field(default_factory=generate_uuid)
