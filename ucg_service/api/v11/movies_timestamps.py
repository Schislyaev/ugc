import uuid

from aiokafka import AIOKafkaProducer
from api.core.config import settings
from api.grpc_src.service.helpers import jwt_check
from fastapi import Body, Header, Request
from fastapi.routing import APIRouter

router = APIRouter()


@router.post(
    path='/film_timecode',
)
async def films_timecode_writes(
    request: Request,
    film_id: uuid.UUID = Body(...),
    timecode: str = Body(description='the moment at which the user is now'),
    access_token: str = Header(...),
):
    user_data = await jwt_check(token=access_token, request_path=request.url)
    producer = AIOKafkaProducer(
        bootstrap_servers=f'{settings.kafka_host}:{settings.kafka_port}'
    )
    await producer.start()
    try:
        await producer.send_and_wait(
            topic=settings.kafka_topic,
            value=bytes(timecode, encoding='utf8'),
            key=bytes(f'{user_data}+{film_id}', encoding='utf8')
            )
    finally:
        await producer.stop()
