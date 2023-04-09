from uuid import UUID

from api.schemas.helpers import MixinModel, UpdateMixinModel
from pydantic import Field


class ReviewModel(MixinModel):
    movie_id: UUID = Field(...)
    review: str = Field(min_length=50, max_length=1000)


class UpdateReviewModel(UpdateMixinModel):
    movie_id: UUID = Field(default=None)
    review: str = Field(min_length=50, max_length=1000)
