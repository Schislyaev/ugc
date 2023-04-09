import random
import time
import uuid

import pymongo
from pymongo import MongoClient

client: MongoClient = pymongo.MongoClient('mongodb://localhost:27017/test')
db = client['test']
collection = db['user_rate']

handred_thousands_ids = [uuid.uuid4() for _ in range(100000)]
bools = [True, False]

count = 0
for user_id in handred_thousands_ids:
    for _ in range(10):
        movie_id = random.choice(handred_thousands_ids)
        is_like = random.choice(bools)
        collection.insert_one({
            'user_id': str(user_id),
            'movie_id': str(movie_id),
            'is_like': is_like,
        })
        count += 1
        print(count)


num: int = db.user_rate.count_documents({})
print(num)

start = time.time()
for _ in db.user_rate.find({'user_id': '0f574a27-8fd6-4ddd-9bb9-74102f08a36a'}):
    pass
res: float = time.time() - start
print(res)

start = time.time()
_ = db.user_rate.count_documents({
    'movie_id': 'c687827f-d5df-4dca-bd1d-8453f57268a2',
    'is_like': True,
})
res = time.time() - start
print(res)

start = time.time()
collection.insert_one({
    'user_id': 'c687827f-d5df-4dca-bd1d-8453f57268a2',
    'movie_id': '0f574a27-8fd6-4ddd-9bb9-74102f08a36a',
    'is_like': True,
})
res = time.time() - start
print(res)
