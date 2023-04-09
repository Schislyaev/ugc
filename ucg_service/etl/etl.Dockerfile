FROM python:3.10.7

WORKDIR /opt/app

RUN pip install poetry

COPY ../pyproject.toml pyproject.toml
COPY ../poetry.lock poetry.lock

RUN poetry config virtualenvs.create false && poetry install

COPY ./etl/core ./core/
COPY ./etl ./etl/

COPY ./etl/etl_entrypoint.sh /

WORKDIR /opt/app

ENTRYPOINT ["sh", "/etl_entrypoint.sh"]
