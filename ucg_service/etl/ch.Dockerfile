#FROM yandex/clickhouse-server:latest

RUN apt update && apt install -y netcat

COPY ch_entrypoint.sh /ch_entrypoint.sh

RUN chmod +x /ch_entrypoint.sh
CMD ["sh", "/ch_entrypoint.sh"]