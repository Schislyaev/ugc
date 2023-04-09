import pathlib

from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_host: str = 'localhost'
    kafka_port: int = 9092
    kafka_topic: str = 'views'
    log_level: str = 'DEBUG'
    project_name: str = 'big data'
    grpc_host: str = 'localhost'
    grpc_port: int = 5051
    mongo_host: str = 'localhost'
    mongo_port: int = 27017

    project_root_path = str(pathlib.Path(__file__).parent.parent)

    sentry_dsn: str = 'https://3ec181e0dd36402fa2d93e20390d9caf@o4504700580790272.ingest.sentry.io/4504700581642240'

    class Config:
        env_file = f'{str(pathlib.Path(__file__).parent.parent.parent)}/.env.example'
        env_file_encoding = 'utf-8'
        case_sensitive = False


settings = Settings()
