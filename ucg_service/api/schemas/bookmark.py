from uuid import UUID

from api.schemas.helpers import MixinModel
from pydantic import BaseModel, Field


class InputBookmarkModel(BaseModel):
    movie_id: UUID = Field(...)


class InternalBookmarkModel(MixinModel):
    movie_id: UUID = Field(...)
    user_id: UUID = Field(default=None)


class BookmarkModel(BaseModel):
    id: UUID = Field(default=None, alias='_id')
    movie_id: UUID = Field(...)


class UpdateBookmarkModel(BaseModel):
    movie_id: UUID = Field(default=None)
