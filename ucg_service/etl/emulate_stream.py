from datetime import datetime
from time import sleep
from uuid import uuid4

from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    api_version=(2, 0, 2),
    acks=1

)

arr = [str(datetime.now().timestamp()).encode('utf-8') for x in range(30)]

# В таком виде не работает в докере
#
# [producer.send(
#     topic='views',
#     value=value,
#     key=bytes(f'{uuid4()}+{uuid4()}', encoding='utf-8'),
# ) for value in arr]


for i, value in enumerate(arr):
    res = producer.send(
        topic='views',
        value=value,
        key=bytes(f'{uuid4()}+{uuid4()}', encoding='utf-8'),
    )
    sleep(0.001)
