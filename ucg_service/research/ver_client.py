import time

import vertica_python

connection_info = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': True,
}

with vertica_python.connect(**connection_info) as connection:
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test (
        id IDENTITY,
        x INTEGER
    )
    """)

    # pack = []
    # for i in range(0, 20000):
    #     pack.append([i])
    #     if i % 5000 == 0:
    #         cursor.executemany(f'INSERT INTO test (x) VALUES (?)', pack, use_prepared_statements=True)
    #         pack = []

    start = time.time()
    cursor.execute('SELECT * FROM test WHERE x=500')
    end = time.time()
    print(end - start)
    for row in cursor.iterate():
        print(row)

    start = time.time()
    cursor.execute('INSERT INTO test (x) VALUES (1000000)')
    end = time.time()
    print(end - start)
