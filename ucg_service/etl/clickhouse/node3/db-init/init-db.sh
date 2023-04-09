#!/bin/bash

set -e

clickhouse client -n <<-EOSQL
    CREATE DATABASE IF NOT EXISTS shard;
    CREATE DATABASE IF NOT EXISTS replica;
    CREATE DATABASE IF NOT EXISTS $CH_DB;
    CREATE TABLE IF NOT EXISTS shard.$CH_TABLE (user_id UUID, movie_id UUID, event_time DateTime64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/$CH_TABLE', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY user_id;
    CREATE TABLE IF NOT EXISTS replica.$CH_TABLE (user_id UUID, movie_id UUID, event_time DateTime64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/$CH_TABLE', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY user_id;
    CREATE TABLE IF NOT EXISTS $CH_DB.$CH_TABLE (user_id UUID, movie_id UUID, event_time DateTime64) ENGINE = Distributed('company_cluster', '', $CH_TABLE, rand());

EOSQL