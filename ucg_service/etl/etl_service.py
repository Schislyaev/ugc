from time import sleep

import backoff
from clickhouse_driver import connect, connection
from clickhouse_driver.errors import Error, ServerException
from etl.core.logger import log
from etl.core.settings import settings
from kafka import KafkaConsumer
from kafka.errors import KafkaError


class ETL:
    def __init__(self):
        self.topic = settings.kafka_topic
        self.kafka_host = settings.kafka_host
        self.kafka_port = settings.kafka_port
        self.consumer = self.connect_kafka_consumer()
        self.consumer.subscribe([f'{self.topic}'])
        self.number_to_poll = 10    # так мало для отладки

        self.ch_host = settings.ch_host
        self.ch_database = settings.ch_db
        self.ch_table = settings.ch_table

        self.logger = log(__name__)

    @backoff.on_exception(
        backoff.expo,
        Error,
        logger=log('ClickHouse >>')
    )
    def connect_clickhouse(self) -> connection:
        conn = connect(
            host=self.ch_host,
            # user='admin',
            # password='123',
            database=self.ch_database
            # self.ch_uri
        )
        return conn

    @backoff.on_exception(
        backoff.expo,
        KafkaError,
        logger=log('Kafka >>')
    )
    def connect_kafka_consumer(self) -> KafkaConsumer:
        consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=[f'{self.kafka_host}:{self.kafka_port}'],
            auto_offset_reset='earliest',
            group_id='echo-messages-to-stdout',
            api_version=(2, 0, 2),
            enable_auto_commit=False,
        )
        return consumer

    @staticmethod
    def transform(chunk):
        for topic_data, consumer_records in chunk:
            transformed_data = [
                (
                    str(message.key.decode('utf-8')).split("+")[0],
                    str(message.key.decode('utf-8')).split("+")[1],
                    round(float((message.value.decode('utf-8'))) * 1000)    # Для сохранения точности до мс
                ) for message in consumer_records
            ]
        return transformed_data

    def load(self, chunk):
        conn = self.connect_clickhouse()
        ch_cursor = conn.cursor()

        try:
            ch_cursor.executemany(
                f'INSERT INTO {self.ch_database}.{self.ch_table} (user_id, movie_id, event_time) VALUES',
                [
                    {
                        'user_id': user_id,
                        'movie_id': movie_id,
                        'event_time': event_time
                     } for user_id, movie_id, event_time in chunk
                ]
            )

            ch_cursor.fetchall()

            # Коммитим при условии записи данных в CH без ошибок
            self.consumer.commit()
        except ServerException as e:
            self.logger.exception(e)
            raise e

    def run(self):
        while True:
            try:
                chunk = self.consumer.poll(max_records=self.number_to_poll)
                # Если в кафке данных нет - ждем две минуты
                if not chunk:
                    sleep(1)
                    continue

                data = self.transform(chunk.items())

                self.load(data)

            except Exception as e:
                self.logger.exception(e)


if __name__ == '__main__':
    etl = ETL()
    etl.run()
