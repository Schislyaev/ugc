import backoff
import sentry_sdk
import uvicorn as uvicorn
from api.core import config
from api.core.logger import LOGGING, log
from api.v11 import bookmarks, marks, movies_timestamps, reviews
from db import mongo
from etl.core.settings import settings
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

logger = log(__name__)

sentry_sdk.init(dsn=config.settings.sentry_dsn, traces_sample_rate=1.0)

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    openapi_tags=[
        {
            'name': 'Bookmarks',
            'description': 'Операции по закладкам пользователя'
        },
        {
            'name': 'Likes',
            'description': 'Операции по оценкам пользователя'
        },
        {
            'name': 'Reviews',
            'description': 'Операции по ревью пользователя'
        },
        {
            'name': 'Timestream',
            'description': 'Операции по потоку временных меток'
        },
    ]
)


app.include_router(movies_timestamps.router, prefix='/api/v11', tags=['Timestream'])
app.include_router(marks.router, prefix='/api/v11', tags=['Likes'])
app.include_router(reviews.router, prefix='/api/v11', tags=['Reviews'])
app.include_router(bookmarks.router, prefix='/api/v11', tags=['Bookmarks'])


@app.on_event('startup')
async def startup():
    mongo.client = AsyncIOMotorClient(
        "mongodb://{host}:{port}".format(
            host=config.settings.mongo_host,
            port=config.settings.mongo_port,
        )
    )


@app.on_event('shutdown')
async def shutdown():
    try:
        mongo.client.close()
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        # log_level=settings.log_level,
        reload=True
    )
