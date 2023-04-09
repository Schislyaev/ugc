import random
import time
import uuid

import psycopg2

DSN = {
    'dbname': 'postgres',
    'user': 'app',
    'password': '1234',
    'host': 'localhost',
    'port': 5432,
}

with psycopg2.connect(**DSN) as conn:
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS user_rate (
        id serial,
        user_id uuid,
        movie_id uuid,
        is_like BOOLEAN
    );''')
    # cur.execute('SELECT * FROM user_rate')

    handred_thousands_ids = [uuid.uuid4() for _ in range(100000)]
    bools = [True, False]

    count = 0
    for user_id in handred_thousands_ids:
        for _ in range(10):
            movie_id = random.choice(handred_thousands_ids)
            is_like = random.choice(bools)
            cur.execute('INSERT INTO user_rate (user_id, movie_id, is_like) VALUES (%s, %s, %s);',
                        (str(user_id), str(movie_id), is_like))
            count += 1
            print(count)
        conn.commit()

    start = time.time()
    cur.execute("SELECT * FROM user_rate WHERE user_id='c08f8ff8-53d3-42ec-ba5e-5800cd710a0c'")
    data = cur.fetchall()
    result = time.time() - start
    print(result)

    start = time.time()
    cur.execute("SELECT COUNT(*) FROM user_rate "
                "WHERE movie_id='7cc01578-eb55-48e7-8796-f4188cf5736a' and is_like=true")
    data = cur.fetchall()
    result = time.time() - start
    print(result)

    cur.execute("EXPLAIN ANALYZE INSERT INTO user_rate (user_id, movie_id, is_like) VALUES "
                "('7cc01578-eb55-48e7-8796-f4188cf5736a', 'c08f8ff8-53d3-42ec-ba5e-5800cd710a0c', true);")
    print(cur.fetchall())
