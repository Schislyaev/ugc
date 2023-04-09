from typing import Literal
from uuid import UUID

from api.schemas.helpers import MixinModel
from pydantic import BaseModel, Field


class MarkModel(MixinModel):
    movie_id: UUID = Field(...)
    mark: Literal[-1, 1]        # int = Field(default=None, le=1, ge=-1)


class UpdateMarkModel(BaseModel):
    movie_id: UUID = Field(default=None)
    mark: int = Field(default=None, le=1, ge=-1)


class InputMarkModel(BaseModel):
    movie_id: UUID = Field(...)
    mark: int = Field(default=None, le=1, ge=-1)
