from api.core.logger import log
from db.mongo import get_client
from fastapi import HTTPException, status
from pymongo.errors import PyMongoError

logger = log(__name__)


class MongoService:
    def __init__(self, db: str, table: str):
        self.db = db
        self.table = table
        self.client = get_client()

    async def add(self, data: dict) -> dict:
        table = self.client[self.db][self.table]
        try:
            new_data = await table.insert_one(data)
            created_data = await table.find_one({'_id': new_data.inserted_id})
        except PyMongoError as error:
            logger.exception(error)
            raise error

        return created_data

    async def get(self, id: str) -> dict:
        try:
            if (data := await self.table.find_one({"_id": id})) is not None:
                return data
        except PyMongoError as error:
            logger.exception()
            raise error

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No element with id = {id}')

    async def update(self, id: str, data: dict) -> dict:
        table = self.client[self.db][self.table]
        try:
            update_result = await table.update_one({'_id': id}, {'$set': data})
            if update_result.modified_count == 1:
                if (updated_data := await table.find_one({'_id': id})) is not None:
                    return updated_data
            if (existing_data := await table.find_one({'_id': id})) is not None:
                return existing_data
        except PyMongoError as error:
            logger.exception(error)
            raise error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No element with id = {id}')

    async def delete(self, id) -> bool:
        table = self.client[self.db][self.table]
        try:
            delete_result = await table.delete_one({'_id': id})
        except PyMongoError as error:
            logger.exception(error)
            raise error
        if delete_result.deleted_count == 1:
            return True

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No element with id = {id}')

    async def get_all_by_userid(self, user_id: str, page: int, size: int):
        table = self.client[self.db][self.table]
        skip = (page - 1) * size
        limit = size
        try:
            results = [record async for record in table.find(
                filter={'user_id': user_id},
                projection={'user_id': 0},
                skip=skip,
                limit=limit
            )]
            return results
        except PyMongoError as error:
            logger.exception(error)
            raise error
