import uuid
from uuid import UUID

import orjson
from bson import ObjectId
from fastapi.param_functions import Query
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MixinModel(BaseModel):
    id: UUID = Field(default=uuid.uuid4(), alias="_id")

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class UpdateMixinModel(BaseModel):
    movie_id: UUID = Field(default=None)

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class InternalModel(MixinModel):
    movie_id: UUID = Field(default=None)
    mark: int = Field(default=None, le=1, ge=-1)
    review: str = Field(default=None, max_length=1000)
    user_id: UUID = Field(default=None)

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Pagination:
    def __init__(
            self,
            number: int = Query(1, alias='page[number]', gt=0, description='Нужная страница (зависит от размера)'),
            size: int = Query(50, alias='page[size]', gt=0, description='Размер записей на странице')
    ):
        self.number = number
        self.size = size
