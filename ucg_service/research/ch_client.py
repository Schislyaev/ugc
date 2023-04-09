import time

from clickhouse_driver import Client

client = Client(host='localhost')

print(client.execute('SHOW DATABASES'))
print(client.execute('CREATE DATABASE IF NOT EXISTS example ON CLUSTER company_cluster'))
print(client.execute('CREATE TABLE IF NOT EXISTS example.regular_table ON CLUSTER company_cluster (id Int64, x Int32)'
                     ' Engine=MergeTree() ORDER BY id'))

# pack = []
# for i in range(1000000):
#     pack.append(f'({i}, {i * 10})')
#     if i % 10000 == 0:
#         client.execute(f'INSERT INTO example.regular_table (id, x) VALUES {", ".join(pack)}')
#         pack = []

start = time.time()
print(client.execute('SELECT * FROM example.regular_table WHERE x=5000000'))
end = time.time()
print(end - start)

start = time.time()
client.execute('INSERT INTO example.regular_table (id, x) VALUES (2000000000, 1)')
end = time.time()
print(end - start)
