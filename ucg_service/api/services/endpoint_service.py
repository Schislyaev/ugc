from api.schemas.helpers import InternalModel
from db.mongo_service import MongoService
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

router = APIRouter()


class EndpointService:
    def __init__(self, db: str, table: str):
        self.db_service = MongoService(
            db=db,
            table=table
        )

    async def post(
        self,
        model: InternalModel,
        user_id: str
    ) -> dict:

        model.user_id = user_id

        model = jsonable_encoder(model)
        model = {k: v for k, v in model.items() if v}
        created_model = await self.db_service.add(data=model)

        return created_model

    async def get(
        self,
        id: str
    ) -> dict:

        model = await self.db_service.get(id=id)
        return jsonable_encoder(model)

    async def update(
        self,
        model: InternalModel,
        id: str
    ) -> dict:

        model = {k: v for k, v in model.dict().items() if v is not None}
        _ = model.pop('id')

        updated_model = await self.db_service.update(id=id, data=model)
        return jsonable_encoder(updated_model)

    async def delete(
        self,
        id: str
    ) -> bool:

        result = await self.db_service.delete(id=id)
        return result

    async def get_all_by_userid(
            self,
            user_id,
            page,
            size
    ) -> list[dict]:

        results = await self.db_service.get_all_by_userid(user_id, page, size)
        return results
