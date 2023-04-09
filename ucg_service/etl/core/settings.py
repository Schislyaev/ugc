import pathlib

from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_topic: str = 'views'
    kafka_host: str = '127.0.0.1'
    kafka_port: int = 9092
    project_name: str = 'big data'

    ch_host: str = 'localhost'
    ch_port: int = 9000
    ch_db: str = 'movies'
    ch_table: str = 'views'

    log_level: str = 'DEBUG'

    project_root_path = str(pathlib.Path(__file__).parent.parent)

    class Config:
        env_file = f'{str(pathlib.Path(__file__).parent.parent.parent)}/.env.example'
        env_file_encoding = 'utf-8'
        case_sensitive = False


settings = Settings()
